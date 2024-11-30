from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    TOKEN: str
    model_config = SettingsConfigDict(env_prefix='BOT_')


class PostgresqlSettings(BaseSettings):
    DB: str
    USER: str
    PASSWORD: str
    HOST: str = "postgresql"
    PORT: str = "5432"
    DRIVER: str = "postgresql+asyncpg"
    model_config = SettingsConfigDict(env_prefix='POSTGRES_')


class PostgresFullSettings(BaseModel):
    postgres: PostgresqlSettings = PostgresqlSettings()
    url: str = f"{postgres.DRIVER}://{postgres.USER}:{postgres.PASSWORD}@{postgres.HOST}:{postgres.PORT}/{postgres.DB}"


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
postgres_settings = PostgresFullSettings()
rabbit_settings = RabbitFullSettings()
