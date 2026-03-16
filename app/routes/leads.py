from fastapi import APIRouter, Query
from app.models.lead import LeadCreate
from app.services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["Leads"])
lead_service = LeadService()


@router.post("/")
def create_lead(payload: LeadCreate):
    return lead_service.create_lead(payload.model_dump())


@router.get("/")
def list_leads(campaign_id: str | None = Query(default=None)):
    return lead_service.list_leads(campaign_id=campaign_id)
