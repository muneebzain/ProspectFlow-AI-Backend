from fastapi import APIRouter, Query, HTTPException

from app.models.lead import LeadCreate
from app.models.outreach import OutreachGenerateRequest
from app.models.workflow import WorkflowUpdateRequest
from app.models.reply import ReplyAnalyzeRequest

from app.services.lead_service import LeadService
from app.services.campaign_service import CampaignService
from app.services.lead_scoring import LeadScoringService
from app.services.lead_enrichment import LeadEnrichmentService
from app.services.outreach_generation import OutreachGenerationService
from app.services.workflow_service import WorkflowService
from app.services.reply_analysis import ReplyAnalysisService
from app.services.reply_workflow_mapper import ReplyWorkflowMapper

router = APIRouter(prefix="/leads", tags=["Leads"])

lead_service = LeadService()
campaign_service = CampaignService()
lead_scoring_service = LeadScoringService()
lead_enrichment_service = LeadEnrichmentService()
outreach_generation_service = OutreachGenerationService()
workflow_service = WorkflowService()
reply_analysis_service = ReplyAnalysisService()
reply_workflow_mapper = ReplyWorkflowMapper()


@router.post("/")
def create_lead(payload: LeadCreate):
    return lead_service.create_lead(payload.model_dump())


@router.get("/")
def list_leads(
    campaign_id: str | None = Query(default=None),
    user_id: str | None = Query(default=None),
):
    return lead_service.list_leads(campaign_id=campaign_id, user_id=user_id)


@router.get("/{lead_id}")
def get_lead(lead_id: str):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead


@router.post("/{lead_id}/enrich")
async def enrich_lead(lead_id: str):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    enrichment_result = await lead_enrichment_service.enrich_lead(lead)

    updated_lead = lead_service.update_lead(
        lead_id,
        {
            **enrichment_result,
            "workflow": {**(lead.get("workflow", {}) or {}), "stage": "enriched"},
        },
    )

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
            "workflow": {**(lead.get("workflow", {}) or {}), "stage": "scored"},
        },
    )

    return updated_lead


@router.post("/{lead_id}/enrich-and-score")
async def enrich_and_score_lead(lead_id: str):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    enrichment_result = await lead_enrichment_service.enrich_lead(lead)

    lead = lead_service.update_lead(
        lead_id,
        {
            **enrichment_result,
            "workflow": {**(lead.get("workflow", {}) or {}), "stage": "enriched"},
        },
    )

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
            "workflow": {**(lead.get("workflow", {}) or {}), "stage": "scored"},
        },
    )

    return updated_lead


@router.post("/{lead_id}/generate-outreach")
def generate_outreach(lead_id: str, payload: OutreachGenerateRequest):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    campaign_id = lead.get("campaign_id")
    campaign = campaign_service.get_campaign_by_id(campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found for this lead")

    outreach_result = outreach_generation_service.generate_outreach(
        lead=lead,
        campaign=campaign,
        channel=payload.channel,
        tone=payload.tone,
    )

    lead_service.update_lead(
        lead_id,
        {
            **outreach_result,
            "workflow": {
                **(lead.get("workflow", {}) or {}),
                "stage": "outreach_generated",
            },
        },
    )

    lead_service.cleanup_old_outreach_fields(lead_id)

    return lead_service.get_lead_by_id(lead_id)


@router.patch("/{lead_id}/workflow")
def update_workflow(lead_id: str, payload: WorkflowUpdateRequest):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    workflow_update = workflow_service.build_workflow_update(
        current_lead=lead, payload=payload.model_dump(exclude_none=True)
    )

    updated_lead = lead_service.update_lead(lead_id, workflow_update)
    return updated_lead


@router.post("/{lead_id}/analyze-reply")
def analyze_reply(lead_id: str, payload: ReplyAnalyzeRequest):
    lead = lead_service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    campaign = campaign_service.get_campaign_by_id(lead.get("campaign_id"))

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found for this lead")

    reply_result = reply_analysis_service.analyze_reply(
        lead=lead,
        campaign=campaign,
        reply_text=payload.reply_text,
    )

    lead = lead_service.update_lead(lead_id, reply_result)

    classification = (lead.get("reply_analysis", {}) or {}).get(
        "classification", "unclear"
    )

    workflow_update = reply_workflow_mapper.build_workflow_from_reply(
        current_lead=lead,
        classification=classification,
    )

    updated_lead = lead_service.update_lead(lead_id, workflow_update)
    return updated_lead
