import json
from typing import Optional

from redis import from_url
from redis.asyncio import Redis

from core.interfaces.cache_interface import ICacheService

class RedisService(ICacheService):
    def __init__(self, redis_url: str):
        self.redis : Redis = from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[dict]:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return

    async def set(self, key: str, value: Optional[dict]) -> None:
        json_value = json.dumps(value)
        await self.redis.set(key, json_value)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
