import os
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

_firestore_client = None


def get_firestore_client():
    global _firestore_client

    if _firestore_client is not None:
        return _firestore_client

    if not firebase_admin._apps:
        cred_path = settings.FIREBASE_CREDENTIALS_PATH

        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()

    _firestore_client = firestore.client(database_id=settings.FIRESTORE_DATABASE_ID)
    return _firestore_client
