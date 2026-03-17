from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: str = "firebase-service-account.json"
    FIRESTORE_DATABASE_ID: str = "(default)"
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
