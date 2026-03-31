from datetime import datetime, timezone


class ReplyWorkflowMapper:
    def build_workflow_from_reply(
        self, current_lead: dict, classification: str
    ) -> dict:
        current_workflow = current_lead.get("workflow", {}) or {}

        workflow = {
            "stage": current_workflow.get("stage", "sent"),
            "outreach_approved": current_workflow.get("outreach_approved", False),
            "sent_status": current_workflow.get("sent_status", "not_sent"),
            "reply_status": "replied",
            "next_follow_up_at": current_workflow.get("next_follow_up_at"),
            "last_contacted_at": current_workflow.get("last_contacted_at"),
            "last_replied_at": datetime.now(timezone.utc),
            "notes": current_workflow.get("notes"),
        }

        if classification == "interested":
            workflow["stage"] = "replied"
        elif classification == "not_interested":
            workflow["stage"] = "closed"
        elif classification == "ask_later":
            workflow["stage"] = "follow_up_needed"
        elif classification == "needs_more_info":
            workflow["stage"] = "replied"
        elif classification == "pricing_request":
            workflow["stage"] = "replied"
        elif classification == "wrong_person":
            workflow["stage"] = "closed"
        elif classification == "booked":
            workflow["stage"] = "booked"
        else:
            workflow["stage"] = "replied"

        return {"workflow": workflow}
