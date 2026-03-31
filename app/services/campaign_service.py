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

        reply_breakdown = {
            "interested": 0,
            "not_interested": 0,
            "ask_later": 0,
            "needs_more_info": 0,
            "pricing_request": 0,
            "wrong_person": 0,
            "booked": 0,
            "unclear": 0,
        }

        tone_performance = {}
        channel_performance = {}

        for doc in docs:
            lead = doc.to_dict() or {}
            total_leads += 1

            if lead.get("score") is not None:
                scored_leads += 1

            workflow = lead.get("workflow", {}) or {}
            outreach = lead.get("outreach", {}) or {}
            reply_analysis = lead.get("reply_analysis", {}) or {}

            if workflow.get("outreach_approved") is True:
                approved_leads += 1

            if workflow.get("sent_status") == "sent":
                sent_leads += 1

            if workflow.get("reply_status") == "replied":
                replied_leads += 1

            if workflow.get("stage") == "booked":
                booked_leads += 1

            classification = reply_analysis.get("classification")
            if classification in reply_breakdown:
                reply_breakdown[classification] += 1

            tone = outreach.get("tone")
            if tone:
                if tone not in tone_performance:
                    tone_performance[tone] = {"generated": 0, "replied": 0, "booked": 0}
                tone_performance[tone]["generated"] += 1
                if workflow.get("reply_status") == "replied":
                    tone_performance[tone]["replied"] += 1
                if workflow.get("stage") == "booked":
                    tone_performance[tone]["booked"] += 1

            channel = outreach.get("channel")
            if channel:
                if channel not in channel_performance:
                    channel_performance[channel] = {
                        "generated": 0,
                        "replied": 0,
                        "booked": 0,
                    }
                channel_performance[channel]["generated"] += 1
                if workflow.get("reply_status") == "replied":
                    channel_performance[channel]["replied"] += 1
                if workflow.get("stage") == "booked":
                    channel_performance[channel]["booked"] += 1

        approval_rate = (
            round((approved_leads / total_leads) * 100, 2) if total_leads > 0 else 0.0
        )
        reply_rate = (
            round((replied_leads / sent_leads) * 100, 2) if sent_leads > 0 else 0.0
        )
        booking_rate = (
            round((booked_leads / replied_leads) * 100, 2) if replied_leads > 0 else 0.0
        )

        for tone, stats in tone_performance.items():
            stats["reply_rate"] = (
                round((stats["replied"] / stats["generated"]) * 100, 2)
                if stats["generated"] > 0
                else 0.0
            )
            stats["booking_rate"] = (
                round((stats["booked"] / stats["replied"]) * 100, 2)
                if stats["replied"] > 0
                else 0.0
            )

        for channel, stats in channel_performance.items():
            stats["reply_rate"] = (
                round((stats["replied"] / stats["generated"]) * 100, 2)
                if stats["generated"] > 0
                else 0.0
            )
            stats["booking_rate"] = (
                round((stats["booked"] / stats["replied"]) * 100, 2)
                if stats["replied"] > 0
                else 0.0
            )

        return {
            "campaign_id": campaign_id,
            "total_leads": total_leads,
            "scored_leads": scored_leads,
            "approved_leads": approved_leads,
            "sent_leads": sent_leads,
            "replied_leads": replied_leads,
            "booked_leads": booked_leads,
            "approval_rate": approval_rate,
            "reply_rate": reply_rate,
            "booking_rate": booking_rate,
            "reply_breakdown": reply_breakdown,
            "tone_performance": tone_performance,
            "channel_performance": channel_performance,
        }

    def get_dashboard_summary(self):
        campaigns = self.list_campaigns()

        total_campaigns = len(campaigns)
        total_leads = 0
        scored_leads = 0
        approved_leads = 0
        sent_leads = 0
        replied_leads = 0
        booked_leads = 0

        overall_reply_breakdown = {
            "interested": 0,
            "not_interested": 0,
            "ask_later": 0,
            "needs_more_info": 0,
            "pricing_request": 0,
            "wrong_person": 0,
            "booked": 0,
            "unclear": 0,
        }

        campaign_breakdown = []

        for campaign in campaigns:
            analytics = self.get_campaign_analytics(campaign["id"])

            total_leads += analytics["total_leads"]
            scored_leads += analytics["scored_leads"]
            approved_leads += analytics["approved_leads"]
            sent_leads += analytics["sent_leads"]
            replied_leads += analytics["replied_leads"]
            booked_leads += analytics["booked_leads"]

            for key in overall_reply_breakdown:
                overall_reply_breakdown[key] += analytics["reply_breakdown"].get(key, 0)

            campaign_breakdown.append(
                {
                    "campaign_id": campaign["id"],
                    "campaign_name": campaign.get("name"),
                    "niche": campaign.get("niche"),
                    "status": campaign.get("status"),
                    "analytics": analytics,
                }
            )

        overall_approval_rate = (
            round((approved_leads / total_leads) * 100, 2) if total_leads > 0 else 0.0
        )
        overall_reply_rate = (
            round((replied_leads / sent_leads) * 100, 2) if sent_leads > 0 else 0.0
        )
        overall_booking_rate = (
            round((booked_leads / replied_leads) * 100, 2) if replied_leads > 0 else 0.0
        )

        return {
            "summary": {
                "total_campaigns": total_campaigns,
                "total_leads": total_leads,
                "scored_leads": scored_leads,
                "approved_leads": approved_leads,
                "sent_leads": sent_leads,
                "replied_leads": replied_leads,
                "booked_leads": booked_leads,
                "overall_approval_rate": overall_approval_rate,
                "overall_reply_rate": overall_reply_rate,
                "overall_booking_rate": overall_booking_rate,
                "overall_reply_breakdown": overall_reply_breakdown,
            },
            "campaigns": campaign_breakdown,
        }
