from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # silently ignore any extra env vars
    )

    # ERCOT
    ercot_subscription_key: str = ""
    ercot_subscription_key_secondary: str = ""
    ercot_username: str = ""
    ercot_password: str = ""
    ercot_base_url: str = "https://api.ercot.com/api/public-reports"

    # ISO-NE
    isone_username: str = ""
    isone_password: str = ""
    isone_base_url: str = "https://webservices.iso-ne.com/api/v1.1"

    # App
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000


settings = Settings()
