from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: str = ""
    FIRESTORE_DATABASE_ID: str = "(default)"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
