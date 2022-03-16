from flasker.redis_client import RedisConn


def reset_app():
    """ A quick and dirty way to reset Redis for the demo. """
    r_client = RedisConn().get_client()
    current_keys = r_client.keys("*")
    for key in current_keys:
        r_client.delete(key)
    return True

