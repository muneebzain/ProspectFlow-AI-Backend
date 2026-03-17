from pydantic import BaseModel
from typing import Optional, List
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

    score: Optional[int] = None
    fit: Optional[str] = None
    reason: Optional[str] = None
    pain_points: Optional[List[str]] = None
    outreach_angle: Optional[str] = None

    website_title: Optional[str] = None
    website_description: Optional[str] = None
    website_text: Optional[str] = None
    website_fetch_status: Optional[str] = None
    company_summary: Optional[str] = None
    inferred_niche: Optional[str] = None
    enriched_pain_points: Optional[List[str]] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
