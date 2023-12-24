from pydantic_settings import BaseSettings, SettingsConfigDict


class LocalStorageConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="local_storage_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    folder_path: str = "."


local_storage_config = LocalStorageConfig()
