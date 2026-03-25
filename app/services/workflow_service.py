from datetime import datetime, timezone


class WorkflowService:
    def build_workflow_update(self, current_lead: dict, payload: dict) -> dict:
        current_workflow = current_lead.get("workflow", {}) or {}

        workflow = {
            "stage": payload.get("stage", current_workflow.get("stage", "new")),
            "outreach_approved": payload.get(
                "outreach_approved", current_workflow.get("outreach_approved", False)
            ),
            "sent_status": payload.get(
                "sent_status", current_workflow.get("sent_status", "not_sent")
            ),
            "reply_status": payload.get(
                "reply_status", current_workflow.get("reply_status", "no_reply")
            ),
            "next_follow_up_at": payload.get(
                "next_follow_up_at", current_workflow.get("next_follow_up_at")
            ),
            "last_contacted_at": current_workflow.get("last_contacted_at"),
            "last_replied_at": current_workflow.get("last_replied_at"),
            "notes": payload.get("notes", current_workflow.get("notes")),
        }

        if workflow["sent_status"] == "sent":
            workflow["last_contacted_at"] = datetime.now(timezone.utc)

        if workflow["reply_status"] == "replied":
            workflow["last_replied_at"] = datetime.now(timezone.utc)

        return {"workflow": workflow}
