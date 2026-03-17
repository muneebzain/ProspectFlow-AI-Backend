from fastapi import APIRouter, Query, HTTPException
from app.models.lead import LeadCreate
from app.services.lead_service import LeadService
from app.services.lead_scoring import LeadScoringService
from app.services.lead_enrichment import LeadEnrichmentService

router = APIRouter(prefix="/leads", tags=["Leads"])
lead_service = LeadService()
lead_scoring_service = LeadScoringService()
lead_enrichment_service = LeadEnrichmentService()


@router.post("/")
def create_lead(payload: LeadCreate):
    return lead_service.create_lead(payload.model_dump())


@router.get("/")
def list_leads(campaign_id: str | None = Query(default=None)):
    return lead_service.list_leads(campaign_id=campaign_id)


@router.post("/{lead_id}/enrich")
async def enrich_lead(lead_id: str):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    enrichment_result = await lead_enrichment_service.enrich_lead(lead)
    updated_lead = lead_service.update_lead(lead_id, enrichment_result)

    return updated_lead


@router.post("/{lead_id}/score")
def score_lead(lead_id: str):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    score_result = lead_scoring_service.score_lead(lead)

    updated_lead = lead_service.update_lead(
        lead_id,
        {
            "score": score_result["score"],
            "fit": score_result["fit"],
            "reason": score_result["reason"],
            "pain_points": score_result["pain_points"],
            "outreach_angle": score_result["outreach_angle"],
            "status": "qualified" if score_result["score"] >= 70 else "review",
        },
    )

    return updated_lead


@router.post("/{lead_id}/enrich-and-score")
async def enrich_and_score_lead(lead_id: str):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    enrichment_result = await lead_enrichment_service.enrich_lead(lead)
    lead = lead_service.update_lead(lead_id, enrichment_result)

    score_result = lead_scoring_service.score_lead(lead)
    updated_lead = lead_service.update_lead(
        lead_id,
        {
            "score": score_result["score"],
            "fit": score_result["fit"],
            "reason": score_result["reason"],
            "pain_points": score_result["pain_points"],
            "outreach_angle": score_result["outreach_angle"],
            "status": "qualified" if score_result["score"] >= 70 else "review",
        },
    )

    return updated_lead
