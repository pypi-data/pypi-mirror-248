from pydantic_settings import BaseSettings, SettingsConfigDict


class WhisperModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="whisper_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    name: str


whisper_config = WhisperModelConfig()  # type: ignore[call-arg]
