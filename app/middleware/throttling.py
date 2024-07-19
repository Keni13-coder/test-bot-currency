from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage
from config.setting import settings



class AntiFloodMiddleware(BaseMiddleware): # Анти спавнинг команд
    
    def __init__(self, storage: RedisStorage) -> None:
       self.storage = storage
       self.expire_time = 1 // settings.MESSAGE_PER_SECOND
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
        ) -> Any:
        user = f'user{event.from_user.id}'
        
        check_user = await self.storage.redis.get(name=user)
        if check_user:
            if int(check_user.decode()) is 1:
                await self.storage.redis.set(name=user, value=1, ex=self.expire_time)
                return await event.answer(f"Многова-то сообщений, давай обожди {self.expire_time} секу")
            
            return
        
        await self.storage.redis.set(name=user, value=1, ex=self.expire_time)
        
        return await handler(event, data)