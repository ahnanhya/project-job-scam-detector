import re


def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    words = text.split()

    return set(words)


def calculate_similarity(
    submitted_text,
    existing_job
):

    submitted_words = clean_text(
        submitted_text
    )

    existing_text = " ".join([
        existing_job.get("title", ""),
        existing_job.get("company", ""),
        existing_job.get("location", ""),
        existing_job.get("snippet", "")
    ])

    existing_words = clean_text(
        existing_text
    )

    if not submitted_words or not existing_words:
        return 0

    common_words = (
        submitted_words &
        existing_words
    )

    union_words = (
        submitted_words |
        existing_words
    )

    similarity = (
        len(common_words) /
        len(union_words)
    ) * 100

    return round(similarity, 2)


def rank_jobs(submitted_text, jobs):

    results = []

    for job in jobs:

        score = calculate_similarity(
            submitted_text,
            job
        )

        job_copy = job.copy()

        job_copy["match_score"] = score

        results.append(job_copy)

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results