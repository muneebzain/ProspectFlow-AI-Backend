from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    campaign_id: str
    full_name: str
    role: str
    company: str
    email: Optional[str] = None
    website: Optional[str] = None
    source: str = "manual"
    status: str = "new"


class LeadResponse(BaseModel):
    id: str
    campaign_id: str
    full_name: str
    role: str
    company: str
    email: Optional[str] = None
    website: Optional[str] = None
    source: str
    status: str
    created_at: Optional[datetime] = None
