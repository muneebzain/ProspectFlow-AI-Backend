ProspectFlow AI

ProspectFlow AI is an AI-powered lead qualification and outreach backend built with FastAPI, Firestore, and Gemini.

It helps businesses organize campaigns, store leads, enrich company data from websites, score lead quality, generate personalized outreach, analyze replies, and track the full outreach workflow.

What ProspectFlow AI does

ProspectFlow AI is designed to support a real outbound sales workflow.

It can:

* create and manage campaigns
* create and manage leads
* enrich leads using website data
* score leads with AI
* generate outreach messages for email and LinkedIn
* track workflow stages such as approved, sent, replied, and booked
* analyze lead replies
* provide campaign analytics and dashboard summaries
* support templates and per-user ownership

Tech Stack

* FastAPI
* Python
* Firebase / Firestore
* Gemini API
* HTTPX
* BeautifulSoup
* Pydantic

Project Structure

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

Main Features by Phase

Phase 1: Foundation

* FastAPI backend setup
* Firestore connection
* campaigns CRUD
* leads CRUD

Phase 2: Lead Scoring

* AI lead scoring
* fit classification
* reasoning and pain points
* outreach angle generation

Phase 3: Lead Enrichment

* website fetch and parsing
* company summary generation
* inferred niche
* enriched pain points

Phase 4: Outreach Generation

* email outreach generation
* LinkedIn outreach generation
* short and medium message variants
* nested outreach object storage

Phase 5: Workflow and Analytics

* workflow tracking
* campaign analytics
* dashboard summary
* approval, sent, replied, and booked states

Phase 6: Reply Intelligence and Optimization

* reply classification
* suggested response generation
* reply breakdown analytics
* tone and channel performance

Phase 7: Productization

* user ownership
* campaign templates
* per-user filtering
* dashboard-ready SaaS structure

Environment Variables

Create a .env file locally based on .env.example.

Example:

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

Download your Firebase service account JSON and place it in the project root.

Example file name:

firebase-service-account.json

5. Create .env

Use the .env.example file as reference and add your real values.

6. Run the backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

7. Open Swagger docs

http://127.0.0.1:8000/docs

Cloud Run Deployment

ProspectFlow AI is designed to be deployed on Google Cloud Run.

Recommended architecture:

* Backend API: Cloud Run
* Database: Firestore
* Future frontend: Firebase Hosting or App Hosting

Deployment files

Make sure these files exist in the project root:

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

Deploy command

gcloud run deploy prospectflow-ai \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FIRESTORE_DATABASE_ID="(default)",GEMINI_MODEL="gemini-2.5-flash" \
  --set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest

Core API Areas

ProspectFlow AI currently includes APIs for:

* campaigns
* leads
* enrichment
* scoring
* outreach generation
* workflow updates
* reply analysis
* campaign analytics
* dashboard summary
* templates

Swagger docs provide the easiest way to test the full API locally or after deployment.

Example Flow

A simple end-to-end test flow looks like this:

1. Create a campaign
2. Create a lead under that campaign
3. Enrich and score the lead
4. Generate outreach
5. Mark outreach as approved and sent
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

* do not commit .env
* do not commit firebase-service-account.json
* do not commit real API keys
* use .env.example instead of real secrets
* rotate any key that may already have been exposed

Current Status

ProspectFlow AI is a backend-first system that is structured like a real SaaS product.

It already supports:

* AI qualification
* AI outreach generation
* reply intelligence
* campaign analytics
* user ownership
* templates
