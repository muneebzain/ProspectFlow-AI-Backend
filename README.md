# ProspectFlow AI
ProspectFlow AI is an AI-powered lead qualification and outreach backend built with FastAPI, Firestore, and Gemini.
It helps businesses organize campaigns, enrich and score leads, generate personalized outreach, analyze replies, and track the full outbound workflow.
## Features
- Campaign and lead management
- Website-based lead enrichment
- AI lead scoring and qualification
- Personalized outreach for email and LinkedIn
- Workflow tracking from new to booked
- Reply analysis and suggested next action
- Campaign analytics and dashboard summaries
- User ownership and reusable campaign templates
## Tech Stack
- Python
- FastAPI
- Firebase / Firestore
- Gemini API
- HTTPX
- BeautifulSoup
- Pydantic
## Project Structure
```bash
prospectflow-ai/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── firebase.py
│   │   └── gemini_client.py
│   ├── models/
│   ├── routes/
│   └── services/
├── requirements.txt
├── Procfile
├── .gcloudignore
├── .env.example
└── README.md

Core Features

1. Lead Qualification

* Store leads under campaigns
* Enrich leads from website data
* Score lead quality with AI
* Save fit, reasoning, pain points, and outreach angle

2. Outreach Generation

* Generate email outreach
* Generate LinkedIn outreach
* Generate short and medium message variants
* Save outreach inside a structured nested object

3. Workflow Tracking

* Track stages such as new, scored, outreach_generated, approved, sent, replied, booked, and closed
* Store notes and follow-up state
* Track sent and replied timestamps

4. Reply Intelligence

* Analyze lead replies
* Classify reply intent
* Suggest next action
* Draft a suggested response

5. Analytics

* Campaign-level analytics
* Dashboard summary across campaigns
* Reply breakdowns
* Tone and channel performance

6. Product-Ready Structure

* Per-user ownership
* Campaign templates
* User-based filtering for leads and campaigns

Environment Variables

Create a local .env file based on .env.example.

FIREBASE_CREDENTIALS_PATH=firebase-service-account.json
FIRESTORE_DATABASE_ID=(default)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

Local Setup

1. Clone the repository

git clone https://github.com/your-username/prospectflow-ai.git
cd prospectflow-ai

2. Create and activate a virtual environment

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Add Firebase credentials

Download your Firebase service account JSON and place it in the project root:

firebase-service-account.json

5. Create .env

Use .env.example as reference and add your real values.

6. Run the backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

7. Open API docs

http://127.0.0.1:8000/docs

Deployment

ProspectFlow AI is designed to be deployed on Google Cloud Run.

Recommended architecture:

* Backend API: Cloud Run
* Database: Firestore
* Future frontend: Firebase Hosting or App Hosting

Required Root Files

* requirements.txt
* Procfile
* .gcloudignore

Procfile

web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

.gcloudignore

.venv
__pycache__
.env
firebase-service-account.json

Cloud Run Deploy Command

gcloud run deploy prospectflow-ai \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FIRESTORE_DATABASE_ID="(default)",GEMINI_MODEL="gemini-2.5-flash" \
  --set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest

Example Flow

1. Create a campaign
2. Create a lead
3. Enrich and score the lead
4. Generate outreach
5. Approve and send outreach
6. Analyze a reply
7. View campaign analytics
8. View dashboard summary

Example Test Data

Campaign

{
  "user_id": "user_001",
  "name": "Shopify Brands Outreach",
  "niche": "Ecommerce / Shopify",
  "offer": "Mobile app development for Shopify brands to increase retention and repeat purchases",
  "status": "draft"
}

Lead

{
  "user_id": "user_001",
  "campaign_id": "PASTE_CAMPAIGN_ID_HERE",
  "full_name": "Sarah Johnson",
  "role": "Founder",
  "company": "Allbirds",
  "email": "sarah@example.com",
  "website": "https://www.allbirds.com",
  "source": "manual",
  "status": "new"
}

Generate Outreach

{
  "channel": "multi",
  "tone": "professional"
}

Analyze Reply

{
  "reply_text": "This looks interesting. Can you send pricing and a few examples?"
}

Firestore Collections

The backend currently uses collections such as:

* campaigns
* leads
* campaign_templates

Security Notes

Before making this repository public:

* Do not commit .env
* Do not commit firebase-service-account.json
* Do not commit real API keys
* Use .env.example instead of real secrets
* Rotate any secret that may already have been exposed

Current Status

ProspectFlow AI is backend-first and already supports:

* AI qualification
* AI outreach generation
* Reply intelligence
* Workflow tracking
* Campaign analytics
* Templates
* Per-user ownership

Recommended next steps:

* Firebase Auth
* Frontend dashboard
* Email sending integration
* LinkedIn sending integration
* Stripe billing
* Audit logs

License

Add your preferred license here.

Example:

MIT License

If you want, I can also give you a more polished GitHub version with badges, a quick-start section, and a demo section.
