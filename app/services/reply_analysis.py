import json
from datetime import datetime, timezone
from app.core.gemini_client import client
from app.core.config import settings


class ReplyAnalysisService:
    def analyze_reply(self, lead: dict, campaign: dict, reply_text: str) -> dict:
        prompt = f"""
You are an expert B2B sales reply analysis assistant.

Analyze this lead reply and return ONLY valid JSON.

Campaign data:
- Campaign name: {campaign.get("name", "")}
- Campaign niche: {campaign.get("niche", "")}
- Campaign offer: {campaign.get("offer", "")}

Lead data:
- Full name: {lead.get("full_name", "")}
- Role: {lead.get("role", "")}
- Company: {lead.get("company", "")}
- Score: {lead.get("score", "")}
- Fit: {lead.get("fit", "")}
- Outreach angle: {lead.get("outreach_angle", "")}

Reply text:
{reply_text}

Return exactly this JSON structure:
{{
  "classification": "interested",
  "sentiment": "positive",
  "reason": "short reason",
  "next_action": "short next action",
  "suggested_response": "short professional reply draft"
}}

Allowed classification values:
- interested
- not_interested
- ask_later
- needs_more_info
- pricing_request
- wrong_person
- booked
- unclear

Allowed sentiment values:
- positive
- neutral
- negative

Rules:
- no markdown
- no explanation outside JSON
- suggested_response should be concise and professional
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
                "reply_analysis": {
                    "reply_text": reply_text,
                    "classification": data.get("classification", "unclear"),
                    "sentiment": data.get("sentiment", "neutral"),
                    "reason": data.get("reason", ""),
                    "next_action": data.get("next_action", ""),
                    "suggested_response": data.get("suggested_response", ""),
                    "analyzed_at": datetime.now(timezone.utc),
                }
            }

        except Exception as e:
            return {
                "reply_analysis": {
                    "reply_text": reply_text,
                    "classification": "unclear",
                    "sentiment": "neutral",
                    "reason": "Reply analysis failed",
                    "next_action": "",
                    "suggested_response": "",
                    "analyzed_at": datetime.now(timezone.utc),
                    "error": str(e),
                }
            }
