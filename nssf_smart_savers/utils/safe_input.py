"""
SmartLife Flexi - Safe Input Validation
Prevents real PII from being entered in demo environment
"""
import re

NIN_PATTERN = re.compile(r'^[A-Z]{2}\d{7}[A-Z]{2}$')
PHONE_PATTERN = re.compile(r'^(\+?256|0)[7][0-9]{8}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')


def looks_like_nin(value: str) -> bool:
    """Return True if value looks like a Uganda NIN."""
    if not value:
        return False
    return bool(NIN_PATTERN.match(str(value).strip().upper()))


def looks_like_phone(value: str) -> bool:
    """Return True if value looks like a Uganda phone number."""
    if not value:
        return False
    cleaned = re.sub(r'[\s\-()]', '', str(value).strip())
    return bool(PHONE_PATTERN.match(cleaned))


def looks_like_email(value: str) -> bool:
    """Return True if value looks like an email address."""
    if not value:
        return False
    return bool(EMAIL_PATTERN.match(str(value).strip()))


def sanitise_demo_text(value: str, max_len: int = 200) -> str:
    """Strip HTML, limit length, reject obvious PII patterns."""
    if not value:
        return ""
    value = str(value)
    value = HTML_TAG_PATTERN.sub('', value)
    value = value[:max_len]
    if looks_like_nin(value) or looks_like_phone(value) or looks_like_email(value):
        return "[PII redacted - demo environment]"
    return value.strip()
