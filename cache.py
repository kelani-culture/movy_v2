from typing import Dict

import redis

from schemas.settings import setting


Setting = setting()
class CacheData:

    def __init__(self):
        self.redis_client = redis.Redis(
            host=Setting.redis_host, port=Setting.redis_port
        )

    def get_hash_data(self, key: str):
        data = self.redis_client.hgetall(key)

        if not data:
            return None
        return data

    def set_hash_data(self, key: str, data: Dict):
        self.redis_client.hset(key=key, mapping=data)

    def close(self):
        self.redis_client.close()
