import json
from app.core.gemini_client import client
from app.core.config import settings


class OutreachGenerationService:
    def generate_outreach(
        self,
        lead: dict,
        campaign: dict,
        channel: str = "multi",
        tone: str = "professional",
    ) -> dict:
        prompt = f"""
You are an expert B2B sales outreach assistant.

Write personalized outreach for this lead and return ONLY valid JSON.

Campaign data:
- Campaign name: {campaign.get("name", "")}
- Campaign niche: {campaign.get("niche", "")}
- Campaign offer: {campaign.get("offer", "")}
- Campaign status: {campaign.get("status", "")}

Lead data:
- Full name: {lead.get("full_name", "")}
- Role: {lead.get("role", "")}
- Company: {lead.get("company", "")}
- Website: {lead.get("website", "")}
- Email: {lead.get("email", "")}
- Score: {lead.get("score", "")}
- Fit: {lead.get("fit", "")}
- Reason: {lead.get("reason", "")}
- Pain points: {lead.get("pain_points", [])}
- Outreach angle: {lead.get("outreach_angle", "")}
- Company summary: {lead.get("company_summary", "")}
- Inferred niche: {lead.get("inferred_niche", "")}
- Enriched pain points: {lead.get("enriched_pain_points", [])}

Requested channel mode: {channel}
Tone: {tone}

Return exactly this JSON structure:
{{
  "email": {{
    "subject": "short subject",
    "message": "personalized email message",
    "follow_up_1": "short email follow up",
    "follow_up_2": "short second email follow up"
  }},
  "linkedin": {{
    "message": "short linkedin first message",
    "follow_up_1": "short linkedin follow up",
    "follow_up_2": "short second linkedin follow up"
  }},
  "variants": {{
    "short": "very short version",
    "medium": "medium length version"
  }}
}}

Rules:
- use the campaign offer naturally
- make the message relevant to campaign niche
- keep language natural and human
- do not sound robotic or too salesy
- email.message under 120 words
- email.follow_up_1 under 80 words
- email.follow_up_2 under 80 words
- linkedin.message under 60 words
- linkedin.follow_up_1 under 50 words
- linkedin.follow_up_2 under 50 words
- variants.short under 35 words
- variants.medium under 80 words
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
                "outreach": {
                    "channel": channel,
                    "tone": tone,
                    "email": {
                        "subject": data.get("email", {}).get("subject", ""),
                        "message": data.get("email", {}).get("message", ""),
                        "follow_up_1": data.get("email", {}).get("follow_up_1", ""),
                        "follow_up_2": data.get("email", {}).get("follow_up_2", ""),
                    },
                    "linkedin": {
                        "message": data.get("linkedin", {}).get("message", ""),
                        "follow_up_1": data.get("linkedin", {}).get("follow_up_1", ""),
                        "follow_up_2": data.get("linkedin", {}).get("follow_up_2", ""),
                    },
                    "variants": {
                        "short": data.get("variants", {}).get("short", ""),
                        "medium": data.get("variants", {}).get("medium", ""),
                    },
                }
            }

        except Exception as e:
            return {
                "outreach": {
                    "channel": channel,
                    "tone": tone,
                    "email": {
                        "subject": "",
                        "message": "",
                        "follow_up_1": "",
                        "follow_up_2": "",
                    },
                    "linkedin": {
                        "message": "",
                        "follow_up_1": "",
                        "follow_up_2": "",
                    },
                    "variants": {
                        "short": "",
                        "medium": "",
                    },
                    "error": str(e),
                }
            }
