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

    root_path: str = ""

    # CORS allowed origins. To specify multiple origins as
    # an environment variable, specify the list as a JSON-encoded string.
    # Example: '["http://localhost:3000", "https://example.com"]
    allow_origins: list[str] = []


config = Config()

__all__ = ["config"]
