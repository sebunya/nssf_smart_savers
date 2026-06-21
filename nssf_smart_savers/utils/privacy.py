"""
SmartLife Flexi - Privacy and PII detection utilities.
Demo environment only.
"""
import re
import json

NIN_PATTERN = re.compile(r'\b[A-Z]{2}\d{7}[A-Z]{2}\b', re.IGNORECASE)
PHONE_PATTERN = re.compile(r'(\+?256|0)[7][0-9]{8}')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b')


def contains_email(value):
    return bool(EMAIL_PATTERN.search(str(value or '')))


def contains_phone(value):
    return bool(PHONE_PATTERN.search(str(value or '').replace(' ', '').replace('-', '')))


def contains_nin_like(value):
    return bool(NIN_PATTERN.search(str(value or '')))


def is_pii_safe(value):
    """Return True if value contains no detectable PII."""
    v = str(value or '')
    return not (contains_email(v) or contains_phone(v) or contains_nin_like(v))


def validate_demo_safe_payload(payload):
    """Raise ValueError if any payload value contains PII."""
    if isinstance(payload, dict):
        for k, v in payload.items():
            if not is_pii_safe(str(v)):
                raise ValueError(f"Demo safety: field '{k}' contains potential PII. Do not submit real personal data.")
    return True


def redact_unsafe_value(value, replacement='[REDACTED]'):
    """Replace detectable PII in a string."""
    value = str(value or '')
    value = EMAIL_PATTERN.sub(replacement, value)
    value = PHONE_PATTERN.sub(replacement, value)
    value = NIN_PATTERN.sub(replacement, value)
    return value


def sanitise_text(value, max_len=200):
    """Strip tags and limit length, redact PII."""
    import re
    value = re.sub(r'<[^>]+>', '', str(value or ''))
    value = value[:max_len]
    return redact_unsafe_value(value)
