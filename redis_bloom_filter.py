import redis
from collections import namedtuple
from flask import Flask

app = Flask(__name__)

RESULTS = namedtuple("RESULTS", "pw bf_unique set_unique bf_unique_count set_unique_count")

BLOOM_FILTER_NAME = "bloom"
SET_NAME = ""

r_client = redis.Redis(host='localhost', port=6379, db=0)


# Note: this is resetting your filters on app start and isn't actually good code outside sandbox
r_client.delete(BLOOM_FILTER_NAME)


@app.route("/")
def hello_world():
    r_client.bf().add(BLOOM_FILTER_NAME, "hello")
    r_client.bf().add(BLOOM_FILTER_NAME, "world")
    foo = r_client.bf().exists(BLOOM_FILTER_NAME, "foo")
    bar = r_client.bf().exists(BLOOM_FILTER_NAME, "bar")
    hello = r_client.bf().exists(BLOOM_FILTER_NAME, "hello")
    world = r_client.bf().exists(BLOOM_FILTER_NAME, "world")
    return f"<p>hello: {hello}</p><p>world: {world}</p><p>foo: {foo}</p><p>bar: {bar}</p>"


GRANDMA_PASSWORDS = [
    'turtle1234',
    'turtle1',
    'turtle1!',
    'turtle',
    'turtle1',
    'turtle1',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
    'turtle1234',
]

ITEM_ADDED_SUCCESSFULLY_BLOOM_FILTER = 1
ITEM_FOUND_IN_BLOOM_FILTER = 1
ITEM_NOT_FOUND_IN_BLOOM_FILTER = 0

ITEM_ADDED_SUCCESSFULLY_SET = 1
ITEM_FOUND_IN_SET = 1
ITEM_NOT_FOUND_IN_SET = 0


def add_bloom_filter(bloom_filter, item):
    """
    Adds item to specified bloom filter.
    Throws AssertionError on None value args

    Keyword arguments:
    bf -- the bloom filter
    pw -- the password to add

    Returns:
    1 if added
    """
    assert bloom_filter is not None
    assert item is not None
    return r_client.bf().add(bloom_filter, item)


@app.route("/add_to_bloom_filter/<bf>/<pw>")
def add_password_bloom_filter(bf, pw):
    """
    Keyword arguments:
    bf -- the bloom filter
    pw -- the password to add

    Return:
    boolean indicating success

    Throws:
    AssertionError on None value args
    """
    result = add_bloom_filter(bf, pw)
    return str(result == ITEM_ADDED_SUCCESSFULLY_BLOOM_FILTER)


def is_in_bloom_filter(bloom_filter, item):
    """
    Checks for item in specified bloom filter.
    Throws AssertionError on None value args

    Keyword arguments:
    bf -- the bloom filter
    pw -- the password to add

    Returns:
    1 if found, 0 if not found
    """
    assert bloom_filter is not None
    assert item is not None
    return r_client.bf().exists(bloom_filter, item)


def is_unique_bloom_filter(bloom_filter, item):
    """
    Converts Redis results to boolean representing if item was unique (aka not found).
    """
    result = is_in_bloom_filter(bloom_filter, item)
    return result == ITEM_NOT_FOUND_IN_BLOOM_FILTER


@app.route("/check_unique_bloom_filter/<bf>/<pw>")
def check_password_unique_bloom_filter(bf, pw):
    """
    Returns str(bool) indicating if item is unique (aka not found).
    String formatting chosen for route display.
    """
    result = is_unique_bloom_filter(bf, pw)
    return str(result)


def add_set(set_name, item):
    assert set_name is not None
    assert item is not None
    return r_client.sadd(set_name, item)


@app.route("/add_to_bloom_filter/<set_name>/<pw>")
def add_password_set(set_name, pw):
    """
    Keyword arguments:
    set_name -- the set name
    pw -- the password to add

    Return:
    str(bool) indicating success
    """
    result = add_set(set_name, pw)
    return str(result == ITEM_ADDED_SUCCESSFULLY_SET)


def is_in_set(set_name, item):
    assert set_name is not None
    assert item is not None
    return r_client.sismember(set_name, item)


def is_unique_set(set_name, item):
    """
    Converts Redis results to boolean representing if item was unique (aka not found).
    """
    result = is_in_set(set_name, item)
    return result == ITEM_NOT_FOUND_IN_SET


@app.route("/check_unique_set/<pw>", defaults={"pw": None})
def check_password_unique_set(set_name, pw):
    result = is_unique_set(set_name, pw)
    return str(result)


@app.route("/check_grandma_passwords")
def check_password():
    """
    Checks a list of grandma's passwords to see how many of her passwords were unique.

    """
    grandma_bloom_filter = "gbloom"
    grandma_set = "gset"
    # Reset the collections (prevents error by creating twice as this is a sandbox)
    r_client.delete(grandma_bloom_filter)
    r_client.delete(grandma_set)
    # Pre-create grandma's bloom filter to specify params
    r_client.bf().create(grandma_bloom_filter, .1, 50)
    set_unique_count = 0
    bf_unique_count = 0
    check_results = list()
    for password in GRANDMA_PASSWORDS:
        unique_to_bf = is_unique_bloom_filter(grandma_bloom_filter, password)
        add_bloom_filter(grandma_bloom_filter, password)
        if unique_to_bf:
            bf_unique_count += 1
        unique_to_set = is_unique_set(grandma_set, password)
        add_set(grandma_set, password)
        if unique_to_set:
            set_unique_count += 1
        password_results = RESULTS(password, unique_to_bf, unique_to_set, bf_unique_count, set_unique_count)
        check_results.append(password_results)
    return {
        "set_unique_count": set_unique_count,
        "bf_unique_count": bf_unique_count,
        "total_count": len(GRANDMA_PASSWORDS),
        "check_results": check_results
    }
