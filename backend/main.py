from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.scam_detector import analyze_job
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

    return {
        "status": "success",
        "data": result
    }


# --------------------------------------------------
# END OF FILE
# --------------------------------------------------