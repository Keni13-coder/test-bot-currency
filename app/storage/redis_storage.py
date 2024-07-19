from abc import ABC, abstractmethod
import json
from typing import Any, AsyncGenerator, Dict, Tuple, TypeVar, Awaitable
from datetime import date, timedelta


import redis.asyncio as aioredis
from config.setting import settings


ResponseData = TypeVar('ResponseData', bound=Tuple[date, Dict])

class Singleton:


    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def _drop(cls) -> None:
        cls._instance = None

class ABCStorage(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def add(self, data) -> None:
        raise NotImplementedError
        
        
    @abstractmethod
    async def fetch_one(self, currency: str) -> ResponseData: 
        raise NotImplementedError
    
    
    @abstractmethod
    async def fetch_all(self) -> list[ResponseData]:
        raise NotImplementedError
    
class AioRedisStorade(ABCStorage, Singleton):
    
    def __init__(self) -> None:
       self._aio_redis = aioredis.from_url(url=settings.redis_uri, protocol=3, decode_responses=True, retry_on_timeout=True)
       
    
    @property
    def aio_redis(self):
        return self._aio_redis
    
    async def _get_gener_data(self) -> AsyncGenerator[ResponseData, None]:
        today = date.today()
        yesterday = today - timedelta(days=1)
        json_to_dict = lambda str_data: json.loads(str_data) 
        
        if (current_data := await self._aio_redis.get(str(today))):
            yield (today, json_to_dict(current_data))
        else:
            (yesterday, json_to_dict(self._aio_redis.get(str(yesterday))))
            
    async def add(self, data) -> None:
       
        await self._aio_redis.set(
                name=str(date.today()),
                value= json.dumps(data).encode(),
                ex=129600
            )

    async def fetch_one(self, currency: str) -> Awaitable[ResponseData]: 

        return await anext(( (date, result_currency) async for date, result_currency in self._get_gener_data() if currency in result_currency), None)
            
    
    async def fetch_all(self) -> Awaitable[list[ResponseData]]:
        return [(date, currency) async for date, currency in self._get_gener_data()]
    
    
    
    

