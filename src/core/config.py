from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_uri: str = ''
    database_name: str = 'tasks'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
