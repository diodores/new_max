#my_project/maxbot_rebbit/src/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_DEFAULT_PORT: int = "5672"
    RABBITMQ_DEFAULT_VHOST: str = "/"

    URL_MAX_API: str
    INSTANCE_ID_MAX: str
    TOKEN_MAX: str

    URL_MAX_WHATSAPP: str
    URL_MAX_WHATSAPP_MEDIA: str
    INSTANCE_ID_WHATSAPP: str
    TOKEN_WHATSAPP: str

    @property
    def RABBITMQ_URL(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USER}:"
            f"{self.RABBITMQ_PASSWORD}@"
            f"{self.RABBITMQ_HOST}:"
            f"{self.RABBITMQ_DEFAULT_PORT}"
            f"{self.RABBITMQ_DEFAULT_VHOST}"
        )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()

