from flasker.redis_client import RedisConn

ITEM_ADDED_SUCCESSFULLY_SET = 1
ITEM_FOUND_IN_SET = 1
ITEM_NOT_FOUND_IN_SET = 0


def add_set(set_name, item):
    assert set_name is not None
    assert item is not None
    r_client = RedisConn().get_client()
    return r_client.sadd(set_name, item)


def add_to_set_format_result(set_name, item):
    """
    Keyword arguments:
    set_name -- the set name
    item -- the item to add

    Return:
    Boolean indicating success
    """
    result = add_set(set_name, item)
    return result == ITEM_ADDED_SUCCESSFULLY_SET


def is_in_set(set_name, item):
    assert set_name is not None
    assert item is not None
    r_client = RedisConn().get_client()
    return r_client.sismember(set_name, item)


def is_unique_set(set_name, item):
    """
    Converts Redis results to boolean representing if item was unique (aka not found).
    """
    result = is_in_set(set_name, item)
    return result == ITEM_NOT_FOUND_IN_SET





