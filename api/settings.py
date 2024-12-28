from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class JWTSettings(BaseSettings):
    ALGORITHM: str
    SECRET: str
    model_config = SettingsConfigDict(env_prefix='API_JWT_')


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


jwt_settings = JWTSettings()
postgres_settings = PostgresFullSettings()

