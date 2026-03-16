from datetime import datetime, timezone
from app.core.firebase import get_firestore_client


class LeadService:
    def __init__(self):
        self.db = get_firestore_client()
        self.collection = self.db.collection("leads")

    def create_lead(self, data: dict):
        payload = {**data, "created_at": datetime.now(timezone.utc)}

        doc_ref = self.collection.document()
        doc_ref.set(payload)

        return {"id": doc_ref.id, **payload}

    def list_leads(self, campaign_id: str | None = None):
        query = self.collection

        if campaign_id:
            query = query.where("campaign_id", "==", campaign_id)

        docs = query.stream()
        results = []

        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            results.append(item)

        return results
