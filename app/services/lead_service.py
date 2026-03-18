from datetime import datetime, timezone
from firebase_admin import firestore
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

    def cleanup_old_outreach_fields(self, lead_id: str):
        doc_ref = self.collection.document(lead_id)
        doc_ref.update(
            {
                "outreach_channel": firestore.DELETE_FIELD,
                "outreach_tone": firestore.DELETE_FIELD,
                "email_subject": firestore.DELETE_FIELD,
                "email_message": firestore.DELETE_FIELD,
                "email_follow_up_1": firestore.DELETE_FIELD,
                "email_follow_up_2": firestore.DELETE_FIELD,
                "linkedin_message": firestore.DELETE_FIELD,
                "linkedin_follow_up_1": firestore.DELETE_FIELD,
                "linkedin_follow_up_2": firestore.DELETE_FIELD,
                "short_message": firestore.DELETE_FIELD,
                "medium_message": firestore.DELETE_FIELD,
                "updated_at": datetime.now(timezone.utc),
            }
        )
