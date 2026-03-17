import json
from app.core.gemini_client import client
from app.core.config import settings


class LeadScoringService:
    def score_lead(self, lead: dict) -> dict:
        prompt = f"""
You are an expert B2B lead qualification assistant.

Analyze this lead and return ONLY valid JSON.

Lead data:
- Full name: {lead.get("full_name", "")}
- Role: {lead.get("role", "")}
- Company: {lead.get("company", "")}
- Website: {lead.get("website", "")}
- Email: {lead.get("email", "")}
- Source: {lead.get("source", "")}
- Campaign ID: {lead.get("campaign_id", "")}
- Company summary: {lead.get("company_summary", "")}
- Inferred niche: {lead.get("inferred_niche", "")}
- Website title: {lead.get("website_title", "")}
- Website description: {lead.get("website_description", "")}
- Enriched pain points: {lead.get("enriched_pain_points", [])}

Return exactly this JSON structure:
{{
  "score": 0,
  "fit": "low",
  "reason": "short reason",
  "pain_points": ["point 1", "point 2"],
  "outreach_angle": "short outreach angle"
}}

Rules:
- score must be between 0 and 100
- fit must be one of: low, medium, high
- pain_points must be an array of 2 to 4 strings
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

            data = json.loads(text)

            return {
                "score": data.get("score", 0),
                "fit": data.get("fit", "low"),
                "reason": data.get("reason", "Scoring unavailable"),
                "pain_points": data.get("pain_points", []),
                "outreach_angle": data.get("outreach_angle", ""),
            }

        except Exception as e:
            return {
                "score": 0,
                "fit": "low",
                "reason": f"Scoring failed: {str(e)}",
                "pain_points": [],
                "outreach_angle": "",
            }
