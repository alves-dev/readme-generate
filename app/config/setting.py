import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GITHUB
    GITHUB_BASE_CLONE_URL: str = 'https://github.com'
    GITHUB_TOKEN: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
