import re


def analyze_job(text):

    text_lower = text.lower()

    score = 0

    signals = []

    scam_dna = []

    explanations = []


    # --------------------------------------------------
    # 1. PROCESSING / REGISTRATION FEE
    # --------------------------------------------------

    fee_words = [
        "processing fee",
        "registration fee",
        "joining fee",
        "security deposit",
        "training fee",
        "application fee",
        "pay a fee",
        "payment required",
        "pay ₹",
        "pay rs",
        "pay rs."
    ]

    fee_found = False

    for word in fee_words:

        if word in text_lower:

            fee_found = True
            break


    if fee_found:

        score += 30

        signals.append("Processing Fee Demand")

        scam_dna.append("PAY")

        explanations.append(
            "The recruiter appears to request money before employment."
        )


    # --------------------------------------------------
    # 2. IMMEDIATE SELECTION
    # --------------------------------------------------

    selection_words = [
        "immediate selection",
        "selected immediately",
        "instant selection",
        "instant joining",
        "selected without interview",
        "no interview",
        "without interview",
        "guaranteed selection"
    ]

    selection_found = False

    for word in selection_words:

        if word in text_lower:

            selection_found = True
            break


    if selection_found:

        score += 20

        signals.append("Immediate Selection")

        scam_dna.append("SELECT")

        explanations.append(
            "The job claims unusually fast or guaranteed selection."
        )


    # --------------------------------------------------
    # 3. UNREALISTIC / HIGH SALARY
    # --------------------------------------------------

    salary_patterns = [
        r"₹\s?[\d,]+\s*(?:per month|monthly)",
        r"rs\.?\s?[\d,]+\s*(?:per month|monthly)",
        r"₹\s?[\d,]+",
        r"rs\.?\s?[\d,]+"
    ]

    salary_found = False

    for pattern in salary_patterns:

        if re.search(pattern, text_lower):

            salary_found = True
            break


    high_salary_words = [
        "high salary",
        "earn huge",
        "earn lakhs",
        "easy income",
        "high income",
        "earn money easily",
        "work from home and earn"
    ]


    if salary_found or any(
        word in text_lower for word in high_salary_words
    ):

        score += 10

        signals.append("Suspicious Salary / Earning Claim")

        explanations.append(
            "The advertisement contains a potentially unrealistic or "
            "aggressive salary or earning claim."
        )


    # --------------------------------------------------
    # 4. NO EXPERIENCE
    # --------------------------------------------------

    experience_words = [
        "no experience",
        "without experience",
        "freshers can apply",
        "anyone can apply",
        "no skills required",
        "no qualification required"
    ]


    if any(word in text_lower for word in experience_words):

        score += 10

        signals.append("No Experience Required")

        explanations.append(
            "The offer emphasizes very low entry requirements."
        )


    # --------------------------------------------------
    # 5. SENSITIVE DOCUMENT REQUEST
    # --------------------------------------------------

    document_words = [
        "aadhaar",
        "aadhar",
        "pan card",
        "pan number",
        "bank account",
        "bank details",
        "account number",
        "otp",
        "password",
        "identity proof",
        "id proof"
    ]


    document_found = False

    for word in document_words:

        if word in text_lower:

            document_found = True
            break


    if document_found:

        score += 25

        signals.append("Sensitive Document Request")

        scam_dna.append("DATA")

        explanations.append(
            "The recruiter requests sensitive personal or financial information."
        )


    # --------------------------------------------------
    # 6. WHATSAPP / TELEGRAM
    # --------------------------------------------------

    messaging_words = [
        "whatsapp",
        "telegram"
    ]


    if any(word in text_lower for word in messaging_words):

        score += 10

        signals.append("Unofficial Messaging Contact")

        explanations.append(
            "Recruitment is being conducted through an informal messaging platform."
        )


    # --------------------------------------------------
    # 7. PERSONAL EMAIL
    # --------------------------------------------------

    personal_email_domains = [
        "@gmail.com",
        "@yahoo.com",
        "@hotmail.com",
        "@outlook.com"
    ]


    personal_email_found = False

    for domain in personal_email_domains:

        if domain in text_lower:

            personal_email_found = True
            break


    if personal_email_found:

        score += 10

        signals.append("Unofficial Contact Email")

        explanations.append(
            "The advertisement contains a personal email domain instead "
            "of an identifiable corporate domain."
        )


    # --------------------------------------------------
    # 8. URGENCY
    # --------------------------------------------------

    urgency_words = [
        "act now",
        "limited time",
        "urgent",
        "immediately",
        "today only",
        "limited slots",
        "respond immediately"
    ]


    if any(word in text_lower for word in urgency_words):

        score += 5

        signals.append("Urgency Pressure")

        explanations.append(
            "The message creates pressure to respond quickly."
        )


    # --------------------------------------------------
    # LIMIT SCORE TO 100
    # --------------------------------------------------

    if score > 100:

        score = 100


    # --------------------------------------------------
    # DETERMINE RISK
    # --------------------------------------------------

    if score >= 70:

        risk = "HIGH RISK"

    elif score >= 40:

        risk = "SUSPICIOUS"

    else:

        risk = "LOW RISK"


    # --------------------------------------------------
    # EXTRACT EMAIL
    # --------------------------------------------------

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )


    # --------------------------------------------------
    # EXTRACT PHONE NUMBERS
    # --------------------------------------------------

    phones = re.findall(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )


    # --------------------------------------------------
    # REMOVE DUPLICATES FROM SCAM DNA
    # --------------------------------------------------

    scam_dna = list(dict.fromkeys(scam_dna))


    # --------------------------------------------------
    # CAMPAIGN INDICATORS
    # --------------------------------------------------

    campaign_indicators = []

    if emails:
        campaign_indicators.append("Email")

    if phones:
        campaign_indicators.append("Phone")

    if "whatsapp" in text_lower:
        campaign_indicators.append("Messaging Platform")


    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {

        "risk_score": score,

        "risk": risk,

        "signals": signals,

        "scam_dna": scam_dna,

        "explanations": explanations,

        "entities": {

            "emails": list(dict.fromkeys(emails)),

            "phones": list(dict.fromkeys(phones))

        },

        "campaign_indicators": campaign_indicators,

        "message": (
            "Potential scam indicators detected."
            if score >= 40
            else "No major scam indicators detected."
        )
    }