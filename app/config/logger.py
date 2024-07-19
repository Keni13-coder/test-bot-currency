import sys
from loguru import logger

from config.setting import settings



logger.remove()
logger.add(sys.stderr, colorize=True, format=settings.LOG_FORMAT)
logger.add(
    "logs/out.log",
    backtrace=True,
    diagnose=True,
    rotation="1 week",
    compression="zip",
    level="ERROR",
    format=settings.LOG_FORMAT,
)
logger.add(
    "logs/api.log",
    rotation="1 week",
    compression="zip",
    format=settings.LOG_FORMAT,
    level=settings.LOG_LEVEL,
)