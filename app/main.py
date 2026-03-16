from fastapi import FastAPI
from app.routes import campaigns, leads

app = FastAPI(title="AI Lead Qualification + Outreach Agent", version="0.1.0")

app.include_router(campaigns.router)
app.include_router(leads.router)


@app.get("/")
def root():
    return {"message": "AI Lead Qualification + Outreach Agent backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
