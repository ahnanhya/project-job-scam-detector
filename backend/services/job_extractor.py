import re


def extract_job_details(text):

    text_lower = text.lower()

    company = ""
    location = ""
    job_title = ""

    # -----------------------------
    # COMPANY
    # -----------------------------

    company_patterns = [
        r"company\s*[:\-]\s*([A-Za-z0-9 &.,]+)",
        r"employer\s*[:\-]\s*([A-Za-z0-9 &.,]+)",
        r"at\s+([A-Z][A-Za-z0-9 &.,]+)"
    ]

    for pattern in company_patterns:
        match = re.search(pattern, text)

        if match:
            company = match.group(1).strip()
            break

    # -----------------------------
    # LOCATION
    # -----------------------------

    common_locations = [
        "Chennai",
        "Coimbatore",
        "Bangalore",
        "Bengaluru",
        "Hyderabad",
        "Mumbai",
        "Delhi",
        "Pune",
        "Kolkata",
        "India",
        "Remote"
    ]

    for place in common_locations:

        if place.lower() in text_lower:
            location = place
            break

    # -----------------------------
    # JOB TITLE
    # -----------------------------

    title_patterns = [
        r"job\s*title\s*[:\-]\s*(.+)",
        r"position\s*[:\-]\s*(.+)",
        r"role\s*[:\-]\s*(.+)",
        r"hiring\s+(.+)"
    ]

    for pattern in title_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            job_title = match.group(1).strip()

            # Limit very long extracted values
            job_title = job_title[:100]

            break

    # -----------------------------
    # FALLBACK JOB TITLE
    # -----------------------------

    if not job_title:

        possible_titles = [
            "software developer",
            "software engineer",
            "web developer",
            "frontend developer",
            "backend developer",
            "full stack developer",
            "data analyst",
            "data scientist",
            "python developer",
            "java developer",
            "data entry",
            "customer support",
            "sales executive",
            "marketing executive",
            "hr executive",
            "e-commerce support executive"
        ]

        for title in possible_titles:

            if title in text_lower:
                job_title = title.title()
                break

    return {
        "job_title": job_title,
        "company": company,
        "location": location
    }