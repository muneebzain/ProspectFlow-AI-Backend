from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CampaignTemplateCreate(BaseModel):
    user_id: str
    name: str
    niche: str
    offer: str
    default_channel: Optional[str] = "multi"
    default_tone: Optional[str] = "professional"


class CampaignTemplateResponse(BaseModel):
    id: str
    user_id: str
    name: str
    niche: str
    offer: str
    default_channel: Optional[str] = "multi"
    default_tone: Optional[str] = "professional"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
