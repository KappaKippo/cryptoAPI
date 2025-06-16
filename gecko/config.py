from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_url: str
    api_token: str
    database_name: str = "coingecko"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
