from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

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


analysis_history = []


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

    analysis_history.append({
        "text": text,
        "data": result,
        "campaign_analysis": campaign_result
    })

    return {
        "status": "success",
        "data": result,
        "campaign_analysis": campaign_result
    }


# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------

@app.get("/dashboard")
def dashboard_overview():
    cases = get_local_campaign_jobs()
    analyzed_jobs = list(analysis_history)

    submitted_cases = []
    for index, analysis in enumerate(analyzed_jobs, start=1):
        analysis_data = analysis.get("data", {})
        campaign_data = analysis.get("campaign_analysis", {})
        submitted_cases.append({
            "id": f"analysis-{index}",
            "title": "Submitted job analysis",
            "company": "User-submitted posting",
            "location": "Not specified",
            "risk": analysis_data.get("risk", "Unknown"),
            "score": analysis_data.get("risk_score", 0),
            "reason": "Analysis result from the current session.",
            "source": "submitted-analysis",
            "campaign_connection": (
                "Potential campaign connection"
                if campaign_data.get("campaign_detected")
                else "No strong campaign connection"
            )
        })

    if not cases:
        return {
            "status": "success",
            "data": {
                "total_analyzed_jobs": len(analyzed_jobs),
                "suspicious_jobs": sum(1 for item in analyzed_jobs if item.get("data", {}).get("risk_score", 0) >= 40),
                "high_risk_jobs": sum(1 for item in analyzed_jobs if item.get("data", {}).get("risk_score", 0) >= 70),
                "potential_campaigns": sum(1 for item in analyzed_jobs if item.get("campaign_analysis", {}).get("campaign_detected")),
                "connected_suspicious_cases": sum(item.get("campaign_analysis", {}).get("connected_cases", 0) for item in analyzed_jobs),
                "shared_indicators": {
                    "phones": [],
                    "payment_ids": [],
                    "emails": [],
                    "domains": [],
                    "behavioral_patterns": []
                },
                "prototype_cases": submitted_cases
            }
        }

    phone_numbers = []
    payment_ids = []
    emails = []
    domains = []
    behavior_patterns = [
        "Urgent hiring language",
        "Advance payment or activation fee",
        "WhatsApp-only recruitment",
        "Remote-only onboarding"
    ]

    for case in cases:
        snippet = (case.get("snippet") or "").lower()

        found_phones = re.findall(r"\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{4}", case.get("snippet") or "")
        for phone in found_phones:
            clean_phone = phone.strip()
            if clean_phone and clean_phone not in phone_numbers:
                phone_numbers.append(clean_phone)

        found_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", case.get("snippet") or "")
        for email in found_emails:
            if email not in emails:
                emails.append(email)

        for domain in re.findall(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", case.get("snippet") or ""):
            normalized = domain.lower()
            if normalized not in domains and not normalized.startswith("http"):
                domains.append(normalized)

        for payment_id in re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", case.get("snippet") or ""):
            if "@" in payment_id and payment_id not in payment_ids:
                payment_ids.append(payment_id)

    suspicious_count = sum(1 for item in analyzed_jobs if item.get("data", {}).get("risk_score", 0) >= 40)
    high_risk_count = sum(
        1 for item in analyzed_jobs
        if item.get("data", {}).get("risk_score", 0) >= 70
    )

    common_cluster_key = "shared-prototype-cluster"
    connected_cases = suspicious_count if suspicious_count else 0

    prototype_cases = list(submitted_cases)
    for case in cases:
        snippet = case.get("snippet") or ""
        reason = "Urgent hiring and advance payment language detected."
        if "whatsapp" in snippet.lower():
            reason = "Recruitment moved to WhatsApp and required upfront payment."
        case_is_high_risk = any(keyword in snippet.lower() for keyword in [
            "fee", "upi", "whatsapp", "urgent", "immediate", "registration", "activation"
        ])
        prototype_cases.append({
            "id": case.get("id"),
            "title": case.get("title"),
            "company": case.get("company"),
            "location": case.get("location"),
            "risk": "High Risk" if case_is_high_risk else "Suspicious",
            "reason": reason,
            "source": case.get("source"),
            "campaign_connection": f"Prototype campaign cluster: {common_cluster_key}"
        })

    return {
        "status": "success",
        "data": {
            "total_analyzed_jobs": len(analyzed_jobs),
            "suspicious_jobs": suspicious_count,
            "high_risk_jobs": high_risk_count,
            "potential_campaigns": (1 if cases else 0) + sum(1 for item in analyzed_jobs if item.get("campaign_analysis", {}).get("campaign_detected")),
            "connected_suspicious_cases": len(cases) + sum(item.get("campaign_analysis", {}).get("connected_cases", 0) for item in analyzed_jobs),
            "shared_indicators": {
                "phones": phone_numbers,
                "payment_ids": payment_ids,
                "emails": emails,
                "domains": domains,
                "behavioral_patterns": behavior_patterns
            },
            "prototype_cases": prototype_cases
        }
    }


# --------------------------------------------------
# END OF FILE
# --------------------------------------------------