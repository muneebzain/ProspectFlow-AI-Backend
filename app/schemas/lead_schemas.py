from typing import Optional

from pydantic import BaseModel, EmailStr


class LeadBase(BaseModel):
    company_name: str
    website: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    source: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadResponse(LeadBase):
    id: int
    score: int
    status: str
    summary: Optional[str] = None
    next_action: Optional[str] = None

    class Config:
        from_attributes = True
