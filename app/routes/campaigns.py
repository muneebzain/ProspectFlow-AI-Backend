from fastapi import APIRouter, HTTPException
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


@router.get("/dashboard/summary")
def get_dashboard_summary():
    return campaign_service.get_dashboard_summary()


@router.get("/{campaign_id}")
def get_campaign(campaign_id: str):
    campaign = campaign_service.get_campaign_by_id(campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return campaign


@router.get("/{campaign_id}/analytics")
def get_campaign_analytics(campaign_id: str):
    campaign = campaign_service.get_campaign_by_id(campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    analytics = campaign_service.get_campaign_analytics(campaign_id)

    return {"campaign": campaign, "analytics": analytics}
