"""Explainable campaign-connection detection for suspicious job postings."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any, Iterable, Mapping

try:
    from services.scam_campaigns import get_local_campaign_jobs
except ImportError:  # pragma: no cover - compatibility when imported as a package
    try:
        from backend.services.scam_campaigns import get_local_campaign_jobs
    except ImportError:  # pragma: no cover
        get_local_campaign_jobs = None


_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_URL_RE = re.compile(r"https?://[^\s)]+|www\.[^\s)]+", re.IGNORECASE)
_DOMAIN_RE = re.compile(r"(?<![@\w])(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?![\w])", re.IGNORECASE)
_PAYMENT_ID_RE = re.compile(
    r"(?:upi|payment\s*(?:id|reference)?|pay(?:ment)?\s+to|payment\s+through)"
    r"\s*[:\-]?\s*([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+|[A-Za-z0-9._%+\-]{5,})",
    re.IGNORECASE,
)

_BEHAVIOR_PATTERNS = {
    "Fee Demand": (
        "registration fee", "application fee", "processing fee", "joining fee",
        "training fee", "onboarding fee", "activation fee", "verification fee",
        "security deposit", "pay a fee", "payment required", "pay upfront",
        "send money", "pay ₹", "pay rs",
    ),
    "Urgent Selection": (
        "immediate selection", "instant selection", "direct selection",
        "selected immediately", "guaranteed selection", "urgent", "immediately",
        "reply now", "act now", "limited seats", "limited slots",
    ),
    "No Interview": (
        "no interview", "without interview", "selected without interview",
    ),
    "WhatsApp Recruitment": ("whatsapp",),
    "Telegram Recruitment": ("telegram",),
    "Document Request": (
        "aadhaar", "aadhar", "pan card", "pan number", "identity proof",
        "id proof", "passport", "kyc", "otp",
    ),
    "Bank Details Request": (
        "bank details", "bank account", "account number", "password",
    ),
    "No Experience Required": (
        "no experience", "without experience", "freshers can apply",
        "anyone can apply", "no skills required", "no qualification required",
    ),
    "Personal Email Recruitment": (
        "@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com",
    ),
    "Unrealistic Salary Claim": (
        "high salary", "earn huge", "earn lakhs", "easy income", "high income",
        "earn money easily", "work from home and earn",
    ),
}


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _normalise_phone(value: Any) -> str:
    digits = re.sub(r"\D", "", _clean_text(value))
    if digits.startswith("0091"):
        digits = digits[2:]
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    return digits if len(digits) == 10 and digits[0] in "6789" else ""


def _extract_phone_numbers(text: str) -> list[str]:
    phones = []
    for match in re.finditer(r"(?:\+?\s*\d[\d().\-\s]{8,}\d)", text or ""):
        phone = _normalise_phone(match.group(0))
        if phone:
            phones.append(phone)
    return list(dict.fromkeys(phones))


def _extract_emails(text: str) -> list[str]:
    return list(dict.fromkeys(match.group(0).lower() for match in _EMAIL_RE.finditer(text or "")))


def _extract_urls(text: str) -> list[str]:
    urls = []
    for match in _URL_RE.finditer(text or ""):
        urls.append(match.group(0).rstrip(".,;:)").lower())
    return list(dict.fromkeys(urls))


def _extract_domains(text: str) -> list[str]:
    email_domains = {email.rsplit("@", 1)[1] for email in _extract_emails(text)}
    domains = []
    for match in _DOMAIN_RE.finditer(text or ""):
        domain = match.group(0).lower().rstrip(".,;:)")
        if domain not in email_domains and not domain.startswith("www."):
            domains.append(domain)
    for url in _extract_urls(text):
        domain_match = re.match(r"https?://([^/]+)|www\.([^/]+)", url)
        if domain_match:
            domain = (domain_match.group(1) or domain_match.group(2)).lower()
            if domain not in domains:
                domains.append(domain)
    return list(dict.fromkeys(domains))


def _extract_payment_ids(text: str) -> list[str]:
    payment_ids = []
    for match in _PAYMENT_ID_RE.finditer(text or ""):
        value = match.group(1).lower().strip(".,;:)")
        if value and value not in payment_ids:
            payment_ids.append(value)
    return payment_ids


def _normalise_entities(entity_map: Mapping[str, Any] | None) -> dict[str, list[str]]:
    entity_map = entity_map if isinstance(entity_map, Mapping) else {}

    def values(*keys: str) -> list[str]:
        result = []
        for key in keys:
            value = entity_map.get(key, [])
            items = value if isinstance(value, (list, tuple, set)) else [value]
            result.extend(_clean_text(item) for item in items if item is not None)
        return result

    emails = [value.lower() for value in values("emails", "email") if value]
    phones = [_normalise_phone(value) for value in values("phones", "phone")]
    payment_ids = [value.lower() for value in values("payment_ids", "payment_id", "upi_ids", "upi_id") if value]
    domains = [value.lower().strip("./") for value in values("domains", "domain") if value]
    urls = [value.lower().rstrip(".,;:)") for value in values("urls", "url") if value]
    return {
        "phones": list(dict.fromkeys(value for value in phones if value)),
        "emails": list(dict.fromkeys(emails)),
        "domains": list(dict.fromkeys(domains)),
        "payment_ids": list(dict.fromkeys(payment_ids)),
        "urls": list(dict.fromkeys(urls)),
    }


def _case_text(case: Mapping[str, Any]) -> str:
    parts = []
    for key in ("title", "company", "location", "salary", "snippet", "source", "type", "text", "message"):
        value = case.get(key)
        if value is not None:
            parts.append(_clean_text(value))
    return " ".join(part for part in parts if part)


def _extract_case_entities(text: str, extra_entities: Mapping[str, Any] | None = None) -> dict[str, list[str]]:
    explicit = _normalise_entities(extra_entities)
    extracted = {
        "phones": _extract_phone_numbers(text),
        "emails": _extract_emails(text),
        "domains": _extract_domains(text),
        "payment_ids": _extract_payment_ids(text),
        "urls": _extract_urls(text),
    }
    return {key: list(dict.fromkeys(explicit[key] + extracted[key])) for key in extracted}


def _extract_behavior_labels(text: str) -> list[str]:
    lowered = (text or "").lower()
    return [
        label for label, phrases in _BEHAVIOR_PATTERNS.items()
        if any(phrase in lowered for phrase in phrases)
    ]


def _text_similarity(left: str, right: str) -> float:
    left_clean = _clean_text(left).lower()
    right_clean = _clean_text(right).lower()
    if not left_clean or not right_clean:
        return 0.0
    return round(SequenceMatcher(None, left_clean, right_clean).ratio() * 100, 2)


def _load_historical_cases() -> list[dict[str, Any]]:
    if get_local_campaign_jobs is None:
        return []
    try:
        cases = get_local_campaign_jobs()
    except Exception:
        return []
    return [case for case in cases if isinstance(case, Mapping)]


def _entity_matches(current: Mapping[str, list[str]], historical: Mapping[str, list[str]]) -> dict[str, list[str]]:
    return {
        key: sorted(set(current.get(key, [])) & set(historical.get(key, [])))
        for key in ("phones", "emails", "domains", "payment_ids", "urls")
    }


def _shared_indicator_objects(shared: Mapping[str, list[str]]) -> list[dict[str, str]]:
    labels = {
        "phones": ("Phone", "Same phone number found in both cases."),
        "emails": ("Email", "Same email address found in both cases."),
        "domains": ("Domain", "Same domain found in both cases."),
        "payment_ids": ("Payment ID", "Same payment or UPI ID found in both cases."),
        "urls": ("URL", "Same URL found in both cases."),
    }
    items = []
    for key, values in shared.items():
        label, reason = labels[key]
        items.extend({"type": label, "value": value, "reason": reason} for value in values)
    return items


def _score_connection(shared: Mapping[str, list[str]], shared_behavior: list[str], similarity: float) -> tuple[int, bool, list[str]]:
    entity_types = [key for key, values in shared.items() if values]
    entity_count = sum(len(values) for values in shared.values())
    reasons = []
    score = 0

    if shared["payment_ids"]:
        score += 55
        reasons.append("Same payment ID found in both cases.")
    if shared["phones"]:
        score += 30
        reasons.append("Same phone number found in both cases.")
    if shared["emails"]:
        score += 30
        reasons.append("Same email address found in both cases.")
    if shared["domains"]:
        score += 25
        reasons.append("Same domain found in both cases.")
    if shared["urls"]:
        score += 20
        reasons.append("Same URL found in both cases.")

    if entity_count > 1:
        score += min(15, (entity_count - 1) * 5)
        reasons.append("Multiple shared indicators strengthen the connection evidence.")
    if shared_behavior:
        score += min(20, len(shared_behavior) * 5)
        reasons.append("Similar recruitment behavior detected.")
    if similarity >= 80:
        score += 15
        reasons.append("Very similar recruitment wording detected.")
    elif similarity >= 65:
        score += 8
        reasons.append("Some recruitment wording is similar.")

    score = min(score, 100)
    has_strong_entity = bool(shared["payment_ids"])
    has_multiple_entities = len(entity_types) >= 2
    has_entity_and_behavior = bool(entity_types) and len(shared_behavior) >= 2
    has_strong_text_pattern = similarity >= 80 and len(shared_behavior) >= 3
    connected = has_strong_entity or has_multiple_entities or has_entity_and_behavior or has_strong_text_pattern
    return score if connected else 0, connected, reasons


def detect_campaign(current_text, current_entities=None, historical_cases=None):
    """Return explainable evidence for potential connections to historical cases."""
    text = _clean_text(current_text)
    empty_result = {
        "status": "NO_CAMPAIGN_CONNECTION",
        "campaign_detected": False,
        "confidence": 0,
        "campaign_confidence": 0,
        "connected_cases": 0,
        "shared_entities": [],
        "shared_behavior": [],
        "connection_reasons": [],
        "matches": [],
        "message": "No job text was submitted for campaign checking." if not text else "No meaningful shared evidence found in historical cases.",
    }
    if not text:
        return empty_result

    cases = historical_cases if historical_cases is not None else _load_historical_cases()
    current = _extract_case_entities(text, current_entities)
    current_behavior = _extract_behavior_labels(text)
    matches = []
    all_shared_entities = []
    all_shared_behavior = set()
    all_reasons = []

    for case in cases or []:
        if not isinstance(case, Mapping):
            continue
        case_text = _case_text(case)
        if not case_text:
            continue
        historical = _extract_case_entities(case_text, case.get("entities"))
        shared = _entity_matches(current, historical)
        shared_behavior = sorted(set(current_behavior) & set(_extract_behavior_labels(case_text)))
        similarity = _text_similarity(text, case_text)
        score, connected, reasons = _score_connection(shared, shared_behavior, similarity)
        if not connected:
            continue

        shared_items = _shared_indicator_objects(shared)
        case_id = str(case.get("id", ""))
        match = {
            "case_id": case_id,
            "title": _clean_text(case.get("title")) or "Historical suspicious case",
            "company": _clean_text(case.get("company")) or "Unknown company",
            "match_score": score,
            "campaign_score": score,
            "similarity": int(round(similarity)),
            "shared_indicators": [item["type"] for item in shared_items],
            "shared_entities": shared_items,
            "shared_behavior": shared_behavior,
            "reasons": reasons,
            "connection_reasons": reasons,
            "historical_case": dict(case),
        }
        matches.append(match)
        all_shared_entities.extend(shared_items)
        all_shared_behavior.update(shared_behavior)
        all_reasons.extend(reasons)

    unique_entities = []
    seen_entities = set()
    for item in all_shared_entities:
        key = (item["type"], item["value"])
        if key not in seen_entities:
            seen_entities.add(key)
            unique_entities.append(item)

    unique_reasons = list(dict.fromkeys(all_reasons))
    confidence = max((match["match_score"] for match in matches), default=0)
    if confidence >= 70:
        status = "STRONG_POTENTIAL_CONNECTION"
    elif matches:
        status = "POTENTIAL_CAMPAIGN"
    else:
        status = "NO_CAMPAIGN_CONNECTION"

    return {
        "status": status,
        "campaign_detected": bool(matches),
        "confidence": confidence,
        "campaign_confidence": confidence,
        "connected_cases": len(matches),
        "shared_entities": unique_entities,
        "shared_behavior": sorted(all_shared_behavior),
        "connection_reasons": unique_reasons,
        "matches": matches,
        "message": (
            "Potential campaign connections found through shared indicators and behavior."
            if matches else
            "No meaningful shared evidence found in historical cases."
        ),
    }


def detect_campaigns(messages: Iterable[Mapping[str, Any] | str], similarity_threshold: float = 0.72, min_size: int = 2):
    """Legacy grouped-detector wrapper retained for older callers."""
    records = []
    for index, item in enumerate(messages or []):
        if isinstance(item, str):
            text = item
            message_id = str(index)
        elif isinstance(item, Mapping):
            text = _clean_text(item.get("text", item.get("message", item.get("snippet", ""))))
            message_id = str(item.get("id", index))
        else:
            continue
        if text:
            records.append({"id": message_id, "snippet": text})

    results = []
    for record in records:
        other_records = [item for item in records if item != record]
        result = detect_campaign(record["snippet"], historical_cases=other_records)
        if result["campaign_detected"]:
            results.append({
                "campaign_id": record["id"],
                "campaign_detected": True,
                "campaign_confidence": result["campaign_confidence"],
                "connected_cases": result["connected_cases"],
                "matches": result["matches"],
            })
    return results


__all__ = ["detect_campaign", "detect_campaigns"]
