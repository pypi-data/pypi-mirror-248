from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class CeleryMessageBusConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="celery_bus_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    broker: Optional[str] = None
    backend: Optional[str] = None
    name: Optional[str] = "celery_message_bus"


celery_bus_config = CeleryMessageBusConfig()
