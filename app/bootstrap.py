import asyncio
from typing import Awaitable, Callable, TypeVar

from storage.redis_storage import  AioRedisStorade

CoroutineType = TypeVar('CoroutineType')

async def bootstrap_job(
    xml_formater: CoroutineType,
    remote_server: CoroutineType,
    upload_job: CoroutineType,
):
    storage = AioRedisStorade()
    remote_task = asyncio.create_task(remote_server(xml_formater))
    return await upload_job(remote_task, storage)
