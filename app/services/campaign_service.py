from datetime import datetime, timezone
from app.core.firebase import get_firestore_client


class CampaignService:
    def __init__(self):
        self.db = get_firestore_client()
        self.collection = self.db.collection("campaigns")

    def create_campaign(self, data: dict):
        payload = {**data, "created_at": datetime.now(timezone.utc)}

        doc_ref = self.collection.document()
        doc_ref.set(payload)

        return {"id": doc_ref.id, **payload}

    def list_campaigns(self):
        docs = self.collection.stream()
        results = []

        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            results.append(item)

        return results
