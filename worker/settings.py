from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    TOKEN: str
    model_config = SettingsConfigDict(env_prefix='BOT_')


class RabbitSettings(BaseSettings):
    HOST: str = "rabbitmq"
    PORT: str = "5672"
    USER: str
    PASSWORD: str
    DRIVER: str = "ampq"
    QUEUE_NAME: str = "words_queue"
    ROUTING_KEY: str = "words_queue"
    model_config = SettingsConfigDict(env_prefix='RABBITMQ_')


class RabbitFullSettings(BaseModel):
    rabbit: RabbitSettings = RabbitSettings()
    url: str = f"{rabbit.DRIVER}://{rabbit.USER}:{rabbit.PASSWORD}@{rabbit.HOST}:{rabbit.PORT}/"


bot_settings = BotSettings()
rabbit_settings = RabbitFullSettings()
