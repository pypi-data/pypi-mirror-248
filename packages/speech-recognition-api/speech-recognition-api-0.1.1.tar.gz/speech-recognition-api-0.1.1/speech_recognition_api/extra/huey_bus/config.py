from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class HueyMessageBusConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="huey_bus_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    redis_host: Optional[str] = "localhost"
    name: Optional[str] = "huey_message_bus"


huey_bus_config = HueyMessageBusConfig()
