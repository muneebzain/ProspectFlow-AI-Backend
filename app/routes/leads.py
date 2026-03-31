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

# keep your existing routes above...


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
