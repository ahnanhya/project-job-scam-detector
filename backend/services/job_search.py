import os
import requests
from dotenv import load_dotenv

from services.scam_campaigns import get_local_campaign_jobs


# Load variables from .env
load_dotenv()


JOOBLE_API_KEY = os.getenv(
    "JOOBLE_API_KEY"
)


def search_jobs(
    keywords,
    location="India"
):

    local_campaign_jobs = get_local_campaign_jobs()

    # Check API key
    if not JOOBLE_API_KEY:

        return {
            "success": True,
            "message": "Jooble API key is not configured. Using local scam campaign database.",
            "total": len(local_campaign_jobs),
            "jobs": local_campaign_jobs
        }


    # Jooble API endpoint
    url = (
        f"https://jooble.org/api/"
        f"{JOOBLE_API_KEY}"
    )


    # Request data
    payload = {

        "keywords": keywords,

        "location": location,

        "page": 1,

        "ResultOnPage": 10,

        "companysearch": False

    }


    try:

        response = requests.post(
            url,
            json=payload,
            timeout=15
        )


        # Check HTTP response
        if response.status_code != 200:

            return {

                "success": False,

                "message":
                    f"Jooble API returned "
                    f"status "
                    f"{response.status_code}.",

                "jobs": []

            }


        # Convert response to JSON
        data = response.json()


        jobs = []


        # Extract jobs
        for job in data.get(
            "jobs",
            []
        ):

            jobs.append({

                "id":
                    job.get(
                        "id"
                    ),

                "title":
                    job.get(
                        "title",
                        ""
                    ),

                "company":
                    job.get(
                        "company",
                        ""
                    ),

                "location":
                    job.get(
                        "location",
                        ""
                    ),

                "salary":
                    job.get(
                        "salary",
                        ""
                    ),

                "snippet":
                    job.get(
                        "snippet",
                        ""
                    ),

                "source":
                    job.get(
                        "source",
                        ""
                    ),

                "link":
                    job.get(
                        "link",
                        ""
                    ),

                "type":
                    job.get(
                        "type",
                        ""
                    ),

                "updated":
                    job.get(
                        "updated",
                        ""
                    )

            })


        return {

            "success": True,

            "total":
                data.get(
                    "totalCount",
                    0
                ),

            "jobs": jobs

        }


    except requests.exceptions.RequestException as error:

        return {

            "success": False,

            "message":
                f"Unable to connect "
                f"to Jooble: {error}",

            "jobs": []

        }