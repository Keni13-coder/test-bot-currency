from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore

import redis.asyncio as aioredis
from bootstrap import bootstrap_job
from logic.upload_job.remote_download_service import get_date_from_bank
from logic.upload_job.xml_service import xml_to_dict
from logic.upload_job.jobs import data_upload_job
from storage.redis_storage import AioRedisStorade
from config.setting import settings
from config.logger import logger
from middleware.storage import StorageMiddleware
from middleware.throttling import AntiFloodMiddleware
from middleware.logging import LoggingMiddleware
from handler.start_handle import start_router


async def main():
    
    async def start_scheduler(job, scheduler: AsyncIOScheduler, args: tuple) -> None:
        
        existing_jobs = scheduler.get_jobs()
        if not existing_jobs:
            await job(*args)
            scheduler.add_job(func=job, trigger='interval',
                          args=args, days=1, misfire_grace_time=60) # minutes days
    
    
    try:
        logger.info('initialization  bot...')
        bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        storage = RedisStorage.from_url(settings.redis_uri)
        jobstores = {
            'default': RedisJobStore(
                jobs_key='dispatched_trips_jobs',
                run_times_key='dispatched_trips_running',
                host=settings.REDIS_HOST_NAME,
                db=settings.REDIS_JOB_DATABASES,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD
            )
        }
        scheduler = AsyncIOScheduler(
            timezone='Europe/Moscow', jobstores=jobstores)
        
        dp = Dispatcher(storage=storage)
        

        aio_redis_storage = AioRedisStorade()
       
        scheduler.start()
        
        await start_scheduler(job=bootstrap_job, scheduler=scheduler, args=(xml_to_dict, get_date_from_bank, data_upload_job))

        dp.update.middleware.register(
            LoggingMiddleware(),
        )
        dp.update.middleware.register(
            StorageMiddleware(storage=aio_redis_storage),
        )
        dp.message.middleware.register(AntiFloodMiddleware(storage=storage))

        dp.include_routers(start_router)

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info('starting bot...')
        await dp.start_polling(bot)

    finally:
        logger.info('close bot...')
        await scheduler.shutdown()
        await aio_redis_storage.aio_redis.aclose()
        await bot.session.close()
        


if __name__ == '__main__':
    import asyncio
  
    asyncio.run(main())
