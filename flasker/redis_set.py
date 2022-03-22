from flasker.redis_client import RedisConn

ITEM_ADDED_SUCCESSFULLY_SET = 1
ITEM_FOUND_IN_SET = 1
ITEM_NOT_FOUND_IN_SET = 0


def add_set(set_name, item):
    """
    Adds item to specified set.

    Keyword arguments:
    set_name -- the set name
    item -- the item to add

    Returns:
    1 if added, 0 if not added
    0 may indicate the item was previously added

    Throws:
    AssertionError on None value args
    """
    assert set_name is not None
    assert item is not None
    r_client = RedisConn().get_client()
    return r_client.sadd(set_name, item)


def add_to_set_format_result(set_name, item):
    """
    Adds items to specified set and formats return as boolean.

    Keyword arguments:
    set_name -- the set name
    item -- the item to add

    Return:
    Boolean indicating success

    Throws:
    AssertionError on None value args
    """
    result = add_set(set_name, item)
    return result == ITEM_ADDED_SUCCESSFULLY_SET


def is_in_set(set_name, item):
    """
    Checks for item in specified set.

    Keyword arguments:
    set_name -- the set
    item -- the item to check

    Returns:
    1 if found, 0 if not found

    Throws:
    AssertionError on None value args
    """
    assert set_name is not None
    assert item is not None
    r_client = RedisConn().get_client()
    return r_client.sismember(set_name, item)


def is_unique_set(set_name, item):
    """
    Converts Redis results to boolean representing if item was unique (aka not found).

    Keyword arguments:
    set_name -- the set
    item -- the item to check

    Returns:
    boolean -- True if unique (aka not found)

    Throws:
    AssertionError on None value args
    """
    result = is_in_set(set_name, item)
    return result == ITEM_NOT_FOUND_IN_SET





