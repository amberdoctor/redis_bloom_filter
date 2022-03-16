import redis
from singleton_decorator import singleton


@singleton
class RedisConn:
    def __init__(self):
        host = 'localhost'
        port = 6379
        self.client = redis.Redis(host=host, port=port, db=0)

    def get_client(self):
        return self.client
