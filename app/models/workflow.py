from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkflowUpdateRequest(BaseModel):
    stage: Optional[str] = None
    outreach_approved: Optional[bool] = None
    sent_status: Optional[str] = None
    reply_status: Optional[str] = None
    next_follow_up_at: Optional[datetime] = None
    notes: Optional[str] = None
