from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    ALGORITHM: str
    SECRET: str
    model_config = SettingsConfigDict(env_prefix='API_JWT_')


jwt_settings = JWTSettings()
