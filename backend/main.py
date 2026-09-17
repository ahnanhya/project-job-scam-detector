from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.scam_detector import analyze_job
from services.scam_campaigns import get_local_campaign_jobs
from services.campaign_detector import detect_campaign
from routes.job_verification import router as job_verification_router


app = FastAPI(
    title="Job Scam Detector API",
    description="Backend API for detecting fraudulent job advertisements and verifying jobs against existing listings",
    version="1.0.0"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# JOB VERIFICATION ROUTES
# --------------------------------------------------

app.include_router(
    job_verification_router
)


# --------------------------------------------------
# HOME / HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Job Scam Detector API is running",
        "status": "success"
    }


# --------------------------------------------------
# EXISTING SCAM ANALYSIS API
# --------------------------------------------------

@app.post("/analyze")
def analyze(job: dict):

    text = job.get(
        "text",
        ""
    )

    if not text.strip():

        return {
            "status": "error",
            "message": "Job description cannot be empty"
        }

    result = analyze_job(text)

    campaign_result = {
        "campaign_detected": False,
        "campaign_confidence": 0,
        "connected_cases": 0,
        "shared_entities": [],
        "shared_behavior": [],
        "matches": [],
        "message": "Campaign analysis unavailable."
    }

    try:
        campaign_result = detect_campaign(
            text,
            result.get("entities", {}),
            get_local_campaign_jobs()
        )
    except Exception:
        campaign_result = {
            "campaign_detected": False,
            "campaign_confidence": 0,
            "connected_cases": 0,
            "shared_entities": [],
            "shared_behavior": [],
            "matches": [],
            "message": "Campaign analysis unavailable."
        }

    return {
        "status": "success",
        "data": result,
        "campaign_analysis": campaign_result
    }


# --------------------------------------------------
# END OF FILE
# --------------------------------------------------