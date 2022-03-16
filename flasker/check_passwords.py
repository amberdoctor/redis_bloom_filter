from collections import namedtuple
from flasker.grandma_passwords import (
    GRANDMA_PASSWORDS,
    GRANDMA_PASSWORDS_FIXED,
)
from flasker.redis_bloom_filter import (
    add_bloom_filter,
    is_unique_bloom_filter,
)
from flasker.redis_set import (
    add_set,
    is_unique_set,
)
from flasker.redis_client import RedisConn


RESULTS = namedtuple("RESULTS", "pw bf_unique set_unique bf_unique_count set_unique_count")


def check_passwords(passwords=GRANDMA_PASSWORDS, error_rate=.2):
    """
    Checks a list of grandma's passwords to see how many of her passwords were unique.

    Keyword Arguments:
    passwords -- a list of passwords
    percent_error -- the error rate (default to .2 or 20%)
    """
    r_client = RedisConn().get_client()
    grandma_bloom_filter = "gbloom"
    grandma_set = "gset"
    # Reset the collections (prevents error by creating twice as this is a sandbox)
    r_client.delete(grandma_bloom_filter)
    r_client.delete(grandma_set)
    # Pre-create grandma's bloom filter to specify params
    r_client.bf().create(grandma_bloom_filter, error_rate, 50)
    set_unique_count = 0
    bf_unique_count = 0
    check_results = list()
    for password in passwords:
        unique_to_bf = is_unique_bloom_filter(grandma_bloom_filter, password)
        add_bloom_filter(grandma_bloom_filter, password)
        if unique_to_bf:
            bf_unique_count += 1
        unique_to_set = is_unique_set(grandma_set, password)
        add_set(grandma_set, password)
        if unique_to_set:
            set_unique_count += 1
        password_results = RESULTS(password, unique_to_bf, unique_to_set, bf_unique_count, set_unique_count)
        check_results.append(str(password_results))  # to string makes the tuple field names print out in the resp.
    return {
        "unique_count_set": set_unique_count,
        "unique_count_bf": bf_unique_count,
        "total_count": len(passwords),
        "check_results": check_results
    }


def check_passwords_fixed():
    """ Changes default params of check_passwords for ease of creating the demo. """
    return check_passwords(passwords=GRANDMA_PASSWORDS_FIXED)


def check_passwords_fixed_error_rate_fixed():
    """ Changes default params of check_passwords for ease of creating the demo. """
    return check_passwords(passwords=GRANDMA_PASSWORDS_FIXED, error_rate=.001)
