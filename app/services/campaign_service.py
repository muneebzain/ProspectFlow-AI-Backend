from datetime import datetime, timezone
from app.core.firebase import get_firestore_client


class CampaignService:
    def __init__(self):
        self.db = get_firestore_client()
        self.collection = self.db.collection("campaigns")

    def create_campaign(self, data: dict):
        doc_ref = self.collection.document()
        now = datetime.now(timezone.utc)

        payload = {"id": doc_ref.id, **data, "created_at": now, "updated_at": now}

        doc_ref.set(payload)
        return payload

    def list_campaigns(self):
        docs = self.collection.stream()
        results = []

        for doc in docs:
            item = doc.to_dict()
            if "id" not in item:
                item["id"] = doc.id
            results.append(item)

        return results

    def get_campaign_by_id(self, campaign_id: str):
        doc_ref = self.collection.document(campaign_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        if "id" not in data:
            data["id"] = doc.id
        return data
