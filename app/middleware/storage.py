from aiogram import BaseMiddleware

from storage.redis_storage import ABCStorage


class StorageMiddleware(BaseMiddleware):
    def __init__(self, storage: ABCStorage):
        super().__init__()
        self.storage = storage

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["storage"] = self.storage
        return await handler(event, data)
