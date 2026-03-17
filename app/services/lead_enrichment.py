import json
from app.core.gemini_client import client
from app.core.config import settings
from app.services.website_enrichment import WebsiteEnrichmentService


class LeadEnrichmentService:
    def __init__(self):
        self.website_service = WebsiteEnrichmentService()

    async def enrich_lead(self, lead: dict) -> dict:
        website_data = await self.website_service.fetch_website_content(
            lead.get("website", "")
        )

        raw_text = website_data.get("website_text") or ""
        raw_title = website_data.get("website_title") or ""
        raw_description = website_data.get("website_description") or ""

        # If nothing useful was fetched, save the website fields and skip AI enrichment
        if not raw_text and not raw_title and not raw_description:
            return {
                "website_title": website_data.get("website_title"),
                "website_description": website_data.get("website_description"),
                "website_text": website_data.get("website_text"),
                "website_fetch_status": website_data.get("website_fetch_status"),
                "company_summary": None,
                "inferred_niche": None,
                "enriched_pain_points": [],
            }

        prompt = f"""
You are a B2B lead enrichment assistant.

Analyze this company information and return ONLY valid JSON.

Lead data:
- Company: {lead.get("company", "")}
- Role: {lead.get("role", "")}
- Website: {lead.get("website", "")}

Website title:
{raw_title}

Website description:
{raw_description}

Website text:
{raw_text}

Return exactly this JSON structure:
{{
  "company_summary": "short summary",
  "inferred_niche": "short niche",
  "enriched_pain_points": ["point 1", "point 2", "point 3"]
}}

Rules:
- company_summary should be short and clear
- inferred_niche should be concise
- enriched_pain_points should contain 2 to 4 items
- no markdown
- no explanation outside JSON
"""

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            ai_data = json.loads(text)

            return {
                "website_title": website_data.get("website_title"),
                "website_description": website_data.get("website_description"),
                "website_text": website_data.get("website_text"),
                "website_fetch_status": website_data.get("website_fetch_status"),
                "company_summary": ai_data.get("company_summary"),
                "inferred_niche": ai_data.get("inferred_niche"),
                "enriched_pain_points": ai_data.get("enriched_pain_points", []),
            }

        except Exception as e:
            return {
                "website_title": website_data.get("website_title"),
                "website_description": website_data.get("website_description"),
                "website_text": website_data.get("website_text"),
                "website_fetch_status": website_data.get("website_fetch_status"),
                "company_summary": None,
                "inferred_niche": None,
                "enriched_pain_points": [],
                "enrichment_error": str(e),
            }
