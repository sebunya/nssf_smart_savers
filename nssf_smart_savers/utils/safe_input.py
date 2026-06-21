"""
SmartLife Flexi - Safe input validation.
Delegates to privacy.py for PII detection.
"""
from nssf_smart_savers.utils.privacy import (
    contains_email,
    contains_phone,
    contains_nin_like,
    sanitise_text,
    redact_unsafe_value,
    is_pii_safe,
)

# Backward compatibility aliases
def looks_like_nin(value):
    return contains_nin_like(value)

def looks_like_phone(value):
    return contains_phone(value)

def looks_like_email(value):
    return contains_email(value)

def sanitise_demo_text(value, max_len=200):
    return sanitise_text(value, max_len)
