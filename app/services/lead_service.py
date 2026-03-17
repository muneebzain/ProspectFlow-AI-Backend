from datetime import datetime, timezone
from app.core.firebase import get_firestore_client


class LeadService:
    def __init__(self):
        self.db = get_firestore_client()
        self.collection = self.db.collection("leads")

    def create_lead(self, data: dict):
        now = datetime.now(timezone.utc)
        doc_ref = self.collection.document()

        payload = {"id": doc_ref.id, **data, "created_at": now, "updated_at": now}

        doc_ref.set(payload)
        return payload

    def list_leads(self, campaign_id: str | None = None):
        query = self.collection

        if campaign_id:
            query = query.where("campaign_id", "==", campaign_id)

        docs = query.stream()
        results = []

        for doc in docs:
            item = doc.to_dict()
            if "id" not in item:
                item["id"] = doc.id
            results.append(item)

        return results

    def get_lead_by_id(self, lead_id: str):
        doc_ref = self.collection.document(lead_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        if "id" not in data:
            data["id"] = doc.id
        return data

    def update_lead(self, lead_id: str, data: dict):
        doc_ref = self.collection.document(lead_id)

        payload = {**data, "updated_at": datetime.now(timezone.utc)}

        doc_ref.update(payload)

        updated_doc = doc_ref.get()
        updated_data = updated_doc.to_dict()
        if "id" not in updated_data:
            updated_data["id"] = updated_doc.id
        return updated_data
