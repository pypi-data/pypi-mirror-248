import redis


class RedisUtil:
    def __init__(self, host, port, password=None, db=0):
        self.redis = redis.Redis(host=host, port=port, password=password, db=db)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        self.redis.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, key):
        return self.redis.get(key)

    def batch_insert(self, data):
        pipeline = self.redis.pipeline()
        for key, value in data.items():
            pipeline.set(key, value)
        pipeline.execute()

    def delete(self, *keys):
        return self.redis.delete(*keys)

    def expire(self, key, time):
        return self.redis.expire(key, time)

    def ttl(self, key):
        return self.redis.ttl(key)

    def keys(self, pattern='*'):
        return self.redis.keys(pattern)
