"""Simple campaign connection detection for suspicious job posts.

This prototype compares a newly submitted job posting with historical scam job
records stored in the backend. It focuses on shared infrastructure such as a
phone number, payment/UPI ID, email address, and repeated scam behaviour.

The logic intentionally stays simple and uses only the Python standard library.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any, Iterable, Mapping

try:
    from services.scam_campaigns import get_local_campaign_jobs
except ImportError:  # pragma: no cover - small compatibility fallback
    try:
        from backend.services.scam_campaigns import get_local_campaign_jobs
    except ImportError:  # pragma: no cover
        get_local_campaign_jobs = None


_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"(?:\+?\s*(?:91|0)?\s*)?([6-9]\d{9})")
_PAYMENT_CONTEXT_RE = re.compile(
    r"(?:upi(?:\s*(?:id|payment\s*id|payment\s*reference|reference|payment\s*to|account))?|"
    r"payment\s*(?:id|reference)|payment\s+to|payment\s+through|upi\s+id)"
    r"\s*[:\-]?\s*([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}|[A-Za-z0-9._@+\-]{5,})",
    re.IGNORECASE,
)


_BEHAVIOR_PATTERNS = {
    "PAYMENT_REQUEST": [
        "registration fee",
        "processing fee",
        "joining fee",
        "training fee",
        "onboarding fee",
        "payment required",
        "security deposit",
        "pay upfront",
        "send money",
        "pay rs",
        "pay ₹",
        "payment to",
        "pay a fee",
    ],
    "FAST_SELECTION": [
        "immediate selection",
        "instant selection",
        "direct selection",
        "no interview",
        "without interview",
        "selected immediately",
        "guaranteed selection",
    ],
    "MESSAGING_APP": [
        "whatsapp",
        "telegram",
    ],
    "REMOTE_JOB": [
        "remote job",
        "work from home",
        "wfh",
        "remote",
    ],
    "DATA_REQUEST": [
        "aadhaar",
        "aadhar",
        "pan card",
        "bank details",
        "bank account",
        "kyc",
        "otp",
        "personal information",
        "identity proof",
        "passport",
    ],
    "URGENCY": [
        "urgent",
        "immediately",
        "reply now",
        "hurry",
        "limited seats",
    ],
}


def _clean_text(text: str) -> str:
    value = text or ""
    value = re.sub(r"https?://\S+|www\.\S+", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _normalise_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    if len(digits) == 10 and digits[0] in "6789":
        return digits
    return ""


def _extract_phone_numbers(text: str) -> list[str]:
    phones: list[str] = []
    for match in _PHONE_RE.finditer(text or ""):
        value = _normalise_phone(match.group(0))
        if value:
            phones.append(value)
    return list(dict.fromkeys(phones))


def _extract_emails(text: str) -> list[str]:
    emails = []
    for match in _EMAIL_RE.finditer(text or ""):
        email = match.group(0).strip().lower()
        emails.append(email)
    return list(dict.fromkeys(emails))


def _extract_payment_ids(text: str) -> list[str]:
    payment_ids: list[str] = []
    text = text or ""
    lower_text = text.lower()
    payment_context_keywords = (
        "upi id",
        "upi payment id",
        "payment id",
        "payment reference",
        "payment to",
        "payment through",
        "upi",
        "reference",
    )
    if not any(keyword in lower_text for keyword in payment_context_keywords):
        return []

    for match in _PAYMENT_CONTEXT_RE.finditer(text):
        value = (match.group(1) or "").strip().lower()
        if not value:
            continue
        if "@" in value:
            if not value.endswith(("@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com")):
                payment_ids.append(value)
            elif "upi" in lower_text or "payment" in lower_text:
                payment_ids.append(value)
        else:
            if len(value) >= 5:
                payment_ids.append(value)

    return list(dict.fromkeys(payment_ids))


def _extract_behavior_labels(text: str) -> list[str]:
    text_lower = (text or "").lower()
    matched = []
    for label, phrases in _BEHAVIOR_PATTERNS.items():
        if any(phrase in text_lower for phrase in phrases):
            matched.append(label)
    return matched


def _text_similarity(left: str, right: str) -> float:
    left_clean = _clean_text(left)
    right_clean = _clean_text(right)
    if not left_clean or not right_clean:
        return 0.0
    ratio = SequenceMatcher(None, left_clean.lower(), right_clean.lower()).ratio()
    return round(ratio * 100, 2)


def _normalise_entities(entity_map: Mapping[str, Any] | None) -> dict[str, list[str]]:
    entity_map = entity_map or {}
    emails = []
    phones = []
    payment_ids = []

    for key in ("emails",):
        value = entity_map.get(key, [])
        if isinstance(value, (list, tuple, set)):
            emails.extend(str(item).strip() for item in value)
        elif value:
            emails.append(str(value).strip())

    for key in ("phones",):
        value = entity_map.get(key, [])
        if isinstance(value, (list, tuple, set)):
            phones.extend(str(item).strip() for item in value)
        elif value:
            phones.append(str(value).strip())

    for key in ("payment_ids", "payment_id", "upi_ids", "upi_id"):
        value = entity_map.get(key, [])
        if isinstance(value, (list, tuple, set)):
            payment_ids.extend(str(item).strip() for item in value)
        elif value:
            payment_ids.append(str(value).strip())

    return {
        "emails": list(dict.fromkeys(email.lower() for email in emails if email)),
        "phones": list(dict.fromkeys(phone for phone in (_normalise_phone(p) for p in phones) if phone)),
        "payment_ids": list(dict.fromkeys(payment_id.lower() for payment_id in payment_ids if payment_id)),
    }


def _extract_case_entities(text: str, extra_entities: Mapping[str, Any] | None = None) -> dict[str, list[str]]:
    entities = _normalise_entities(extra_entities)
    entities["emails"] = list(dict.fromkeys(entities["emails"] + _extract_emails(text)))
    entities["phones"] = list(dict.fromkeys(entities["phones"] + _extract_phone_numbers(text)))
    entities["payment_ids"] = list(dict.fromkeys(entities["payment_ids"] + _extract_payment_ids(text)))
    return entities


def _load_historical_cases() -> list[dict[str, Any]]:
    if get_local_campaign_jobs is not None:
        try:
            return list(get_local_campaign_jobs())
        except Exception:
            return []
    return []


def detect_campaign(
    current_text,
    current_entities=None,
    historical_cases=None,
):
    """Check whether a current job posting appears connected to historical scam cases."""
    if current_text is None:
        current_text = ""
    current_text = str(current_text)
    if not current_text.strip():
        return {
            "campaign_detected": False,
            "campaign_confidence": 0,
            "connected_cases": 0,
            "shared_entities": [],
            "shared_behavior": [],
            "matches": [],
            "message": "No job text was submitted for campaign checking.",
        }

    if historical_cases is None:
        historical_cases = _load_historical_cases()

    current_entities = _extract_case_entities(current_text, current_entities)
    current_behaviors = _extract_behavior_labels(current_text)

    shared_entities_list = []
    shared_behavior_set = set()
    matches = []

    for historical_case in historical_cases or []:
        if not isinstance(historical_case, dict):
            continue

        case_text = historical_case.get("snippet") or historical_case.get("title") or historical_case.get("company") or ""
        case_entities = _extract_case_entities(str(case_text), historical_case)
        case_behaviors = _extract_behavior_labels(str(case_text))

        shared_phones = sorted(set(current_entities["phones"]) & set(case_entities["phones"]))
        shared_emails = sorted(set(current_entities["emails"]) & set(case_entities["emails"]))
        shared_payment_ids = sorted(set(current_entities["payment_ids"]) & set(case_entities["payment_ids"]))
        shared_behavior = sorted(set(current_behaviors) & set(case_behaviors))

        shared_items = []
        for value in shared_phones:
            shared_items.append({
                "type": "Phone",
                "value": value,
                "reason": "Same phone number found in another scam case.",
            })
        for value in shared_emails:
            shared_items.append({
                "type": "Email",
                "value": value,
                "reason": "Same email address found in another scam case.",
            })
        for value in shared_payment_ids:
            shared_items.append({
                "type": "Payment ID",
                "value": value,
                "reason": "Same payment or UPI ID found in another scam case.",
            })

        similarity = _text_similarity(current_text, str(case_text))
        score = 0
        if shared_phones:
            score += 40
        if shared_payment_ids:
            score += 40
        if shared_emails:
            score += 30
        score += len(shared_behavior) * 5
        if similarity >= 70:
            score += 10
        score = min(score, 100)

        matched = bool(shared_phones or shared_emails or shared_payment_ids or shared_behavior or similarity >= 70)
        if matched and score > 0:
            for item in shared_items:
                shared_entities_list.append(item)
            shared_behavior_set.update(shared_behavior)

            matches.append({
                "campaign_score": int(score),
                "similarity": int(round(similarity)),
                "shared_entities": shared_items,
                "shared_behavior": shared_behavior,
                "historical_case": historical_case,
            })

    unique_shared_entities = []
    seen = set()
    for item in shared_entities_list:
        key = (item["type"], item["value"])
        if key not in seen:
            seen.add(key)
            unique_shared_entities.append(item)

    if matches:
        campaign_confidence = max(match["campaign_score"] for match in matches)
        campaign_detected = True
        message = "Potential connection to existing scam campaigns found."
    else:
        campaign_confidence = 0
        campaign_detected = False
        message = "No strong campaign connection found in current historical scam records."

    return {
        "campaign_detected": campaign_detected,
        "campaign_confidence": int(campaign_confidence),
        "connected_cases": len(matches),
        "shared_entities": unique_shared_entities,
        "shared_behavior": sorted(shared_behavior_set),
        "matches": matches,
        "message": message,
    }


def detect_campaigns(
    messages: Iterable[Mapping[str, Any] | str],
    similarity_threshold: float = 0.72,
    min_size: int = 2,
):
    """Legacy compatibility wrapper for grouped campaign detection.

    This keeps the earlier function name working for any older code that still
    expects the original group-based detector.
    """
    records = []
    for index, item in enumerate(messages):
        if isinstance(item, str):
            text_value = item
            message_id = str(index)
        else:
            text_value = str(item.get("text", item.get("message", "")))
            message_id = str(item.get("id", index))
        if text_value.strip():
            records.append({"id": message_id, "snippet": text_value})

    results = []
    for record in records:
        result = detect_campaign(record["snippet"], historical_cases=records)
        if result["campaign_detected"]:
            results.append({
                "campaign_id": record["id"],
                "campaign_detected": result["campaign_detected"],
                "campaign_confidence": result["campaign_confidence"],
                "connected_cases": result["connected_cases"],
                "matches": result["matches"],
            })
    return results


__all__ = ["detect_campaign", "detect_campaigns"]
