from datetime import datetime, timezone
from app.core.firebase import get_firestore_client


class CampaignService:
    def __init__(self):
        self.db = get_firestore_client()
        self.collection = self.db.collection("campaigns")
        self.leads_collection = self.db.collection("leads")

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

    def get_campaign_analytics(self, campaign_id: str):
        docs = self.leads_collection.where("campaign_id", "==", campaign_id).stream()

        total_leads = 0
        scored_leads = 0
        approved_leads = 0
        sent_leads = 0
        replied_leads = 0
        booked_leads = 0

        for doc in docs:
            lead = doc.to_dict() or {}
            total_leads += 1

            if lead.get("score") is not None:
                scored_leads += 1

            workflow = lead.get("workflow", {}) or {}

            if workflow.get("outreach_approved") is True:
                approved_leads += 1

            if workflow.get("sent_status") == "sent":
                sent_leads += 1

            if workflow.get("reply_status") == "replied":
                replied_leads += 1

            if workflow.get("stage") == "booked":
                booked_leads += 1

        return {
            "campaign_id": campaign_id,
            "total_leads": total_leads,
            "scored_leads": scored_leads,
            "approved_leads": approved_leads,
            "sent_leads": sent_leads,
            "replied_leads": replied_leads,
            "booked_leads": booked_leads,
        }
