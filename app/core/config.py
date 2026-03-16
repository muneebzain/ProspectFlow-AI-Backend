import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    FIRESTORE_DATABASE_ID: str = os.getenv("FIRESTORE_DATABASE_ID", "(default)")


settings = Settings()
