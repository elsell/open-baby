from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="",
        case_sensitive=False,
    )

    # Define your settings here, for example:
    database_url: str = "sqlite:///./test.db"
    debug: bool = False


config = Config()

__all__ = ["config"]
