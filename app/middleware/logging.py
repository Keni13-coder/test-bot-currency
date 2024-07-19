from mailbox import Message
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from config.logger import logger

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
        ) -> Any:
        
        try:
            result = await handler(event, data)
            logger.info(event.message.text)
            return result
        except BaseException as ex:
            logger.exception(ex)