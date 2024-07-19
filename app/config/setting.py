from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Settings(BaseSettings):
    
    # log region
    LOG_LEVEL: str = Field(default=LogLevel.DEBUG)
    LOG_FORMAT: str = Field(
        title="формат для logger",
        default="<level>{level}</level> | <magenta>{time:%Y-%m-%d %H:%M:%S}</magenta> | <level>{message}</level>",
    )
    # end region
    
    
    # bot region
    BOT_TOKEN: str
    MESSAGE_PER_SECOND: int = Field(
        title="Кол-во сообщений в секунду", default=1)
    # end region
    
    
    # redis region
    REDIS_CONNECT_METHOD: str = Field(default='redis')
    REDIS_HOST_NAME: str = Field(default='localhost')
    REDIS_PASSWORD: str = Field(default='')
    REDIS_PORT: int = Field(default=6379)
    REDIS_DATABASES: int = Field(default=0)
    REDIS_JOB_DATABASES: int = Field(default=1)
    # end region
    @property
    def redis_uri(self):
        uri = (
            f'{self.REDIS_CONNECT_METHOD}://{self.REDIS_PASSWORD}@' + \
            f'{self.REDIS_HOST_NAME}:{self.REDIS_PORT}/{self.REDIS_DATABASES}'
            )
        return uri
    
    model_config = SettingsConfigDict(env_file=".env")
    

settings = Settings()