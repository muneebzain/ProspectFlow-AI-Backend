from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EmailOutreach(BaseModel):
    subject: Optional[str] = None
    message: Optional[str] = None
    follow_up_1: Optional[str] = None
    follow_up_2: Optional[str] = None


class LinkedInOutreach(BaseModel):
    message: Optional[str] = None
    follow_up_1: Optional[str] = None
    follow_up_2: Optional[str] = None


class OutreachVariants(BaseModel):
    short: Optional[str] = None
    medium: Optional[str] = None


class OutreachData(BaseModel):
    channel: Optional[str] = None
    tone: Optional[str] = None
    email: Optional[EmailOutreach] = None
    linkedin: Optional[LinkedInOutreach] = None
    variants: Optional[OutreachVariants] = None
    error: Optional[str] = None


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

    outreach: Optional[OutreachData] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
