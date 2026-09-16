from fastapi import APIRouter

from services.job_extractor import extract_job_details
from services.job_search import search_jobs
from services.job_matcher import rank_jobs
from services.scam_detector import analyze_job
from services.scam_campaigns import get_local_campaign_jobs


router = APIRouter()


@router.post("/verify-job")
def verify_job(data: dict):

    text = data.get("text", "")

    if not text.strip():

        return {
            "status": "error",
            "message": "Job content cannot be empty."
        }

    # -----------------------------
    # STEP 1
    # Extract job information
    # -----------------------------

    job_details = extract_job_details(text)

    job_title = job_details.get(
        "job_title",
        ""
    )

    location = job_details.get(
        "location",
        ""
    )

    company = job_details.get(
        "company",
        ""
    )

    # -----------------------------
    # STEP 2
    # Build search query
    # -----------------------------

    search_keywords = job_title

    if company:

        search_keywords += " " + company

    if not search_keywords.strip():

        search_keywords = text[:100]

    search_location = (
        location
        if location
        else "India"
    )

    # -----------------------------
    # STEP 3
    # Search live jobs
    # -----------------------------

    search_result = search_jobs(
        search_keywords,
        search_location
    )

    if not search_result.get("success"):

        return {
            "status": "error",
            "message": search_result.get(
                "message",
                "Job search failed."
            )
        }

    jobs = search_result.get(
        "jobs",
        []
    )

    if not jobs:
        jobs = get_local_campaign_jobs()

    all_jobs = list(jobs) + get_local_campaign_jobs()

    # -----------------------------
    # STEP 4
    # Match jobs
    # -----------------------------

    matched_jobs = rank_jobs(
        text,
        all_jobs
    )

    # -----------------------------
    # STEP 5
    # Existing scam detector
    # -----------------------------

    scam_result = analyze_job(text)

    # -----------------------------
    # STEP 6
    # Determine match status
    # -----------------------------

    if len(matched_jobs) == 0:

        match_status = (
            "NO MATCHING JOB FOUND"
        )

    else:

        best_score = matched_jobs[0][
            "match_score"
        ]

        if best_score >= 40:

            match_status = (
                "SIMILAR JOBS FOUND"
            )

        else:

            match_status = (
                "LOW SIMILARITY"
            )

    return {

        "status": "success",

        "submitted_job": {
            "job_title": job_title,
            "company": company,
            "location": location
        },

        "job_search": {
            "keywords": search_keywords,
            "location": search_location,
            "total_found": search_result.get(
                "total",
                0
            ),
            "match_status": match_status
        },

        "matching_jobs": matched_jobs[:5],

        "scam_analysis": scam_result

    }