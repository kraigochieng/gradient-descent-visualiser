from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import find_dotenv


class Settings(BaseSettings):
    client_url: str
    nuxt_public_api_base: str

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra="allow")


settings = Settings()
