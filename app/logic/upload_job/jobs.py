from typing import Awaitable

from storage.redis_storage import ABCStorage
from config.logger import logger


async def data_upload_job(remote_service: Awaitable[dict], storage: ABCStorage) -> None:
    try:
        data: dict = await remote_service
        await storage.add(data)
        logger.info('job data_upload_job has been completed')
    except BaseException as ex:
        logger.error('job data_upload_job failed with an error')
        logger.exception(ex)