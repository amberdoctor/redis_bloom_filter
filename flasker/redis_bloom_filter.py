from flasker.redis_client import RedisConn

ITEM_ADDED_SUCCESSFULLY_BLOOM_FILTER = 1
ITEM_FOUND_IN_BLOOM_FILTER = 1
ITEM_NOT_FOUND_IN_BLOOM_FILTER = 0


def add_bloom_filter(bloom_filter, item):
    """
    Adds item to specified bloom filter.

    Keyword arguments:
    bloom_filter -- the bloom filter
    item -- the item to add

    Returns:
    1 if added, 0 if not added
    0 may indicate the item was previously added

    Throws:
    AssertionError on None value args
    """
    assert bloom_filter is not None
    assert item is not None
    r_client = RedisConn().get_client()
    return r_client.bf().add(bloom_filter, item)


def add_to_bloom_filter_format_result(bloom_filter, item):
    """
    Adds items to specified bloom filter and formats return as boolean.

    Keyword arguments:
    bloom_filter -- the bloom filter
    item -- the item to add

    Return:
    boolean indicating success

    Throws:
    AssertionError on None value args
    """
    result = add_bloom_filter(bloom_filter, item)
    return result == ITEM_ADDED_SUCCESSFULLY_BLOOM_FILTER


def is_in_bloom_filter(bloom_filter, item):
    """
    Checks for item in specified bloom filter.

    Keyword arguments:
    bloom_filter -- the bloom filter
    item -- the item to check

    Returns:
    1 if found, 0 if not found

    Throws:
    AssertionError on None value args
    """
    assert bloom_filter is not None
    assert item is not None
    r_client = RedisConn().get_client()
    return r_client.bf().exists(bloom_filter, item)


def is_unique_bloom_filter(bloom_filter, item):
    """
    Converts Redis results to boolean representing if item was unique (aka not found).

    Keyword arguments:
    bloom_filter -- the bloom filter
    item -- the item to check

    Returns:
    boolean -- True if unique (aka not found)

    Throws:
    AssertionError on None value args
    """
    result = is_in_bloom_filter(bloom_filter, item)
    return result == ITEM_NOT_FOUND_IN_BLOOM_FILTER
