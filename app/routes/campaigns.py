from fastapi import APIRouter
from app.models.campaign import CampaignCreate
from app.services.campaign_service import CampaignService

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])
campaign_service = CampaignService()


@router.post("/")
def create_campaign(payload: CampaignCreate):
    return campaign_service.create_campaign(payload.model_dump())


@router.get("/")
def list_campaigns():
    return campaign_service.list_campaigns()
