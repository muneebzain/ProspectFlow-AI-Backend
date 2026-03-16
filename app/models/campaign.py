from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CampaignCreate(BaseModel):
    name: str
    niche: str
    offer: str
    status: str = "draft"


class CampaignResponse(BaseModel):
    id: str
    name: str
    niche: str
    offer: str
    status: str
    created_at: Optional[datetime] = None
