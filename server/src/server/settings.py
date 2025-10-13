from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import find_dotenv


class Settings(BaseSettings):
    client_url: str

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra="allow")


settings = Settings()
