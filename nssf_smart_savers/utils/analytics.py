"""
SmartLife Flexi - Analytics Utilities
Demo environment - GTM/GA4 event sanitisation
"""

ALLOWED_PARAMS = [
    "journey_type",
    "segment",
    "goal_category",
    "frequency",
    "period_band",
    "target_band",
    "source_category",
    "industry_category",
    "country_band",
    "step_name",
    "staff_assisted",
    "payment_status",
    "completion_status",
    "dropoff_step",
    "lead_stage",
]


def sanitise_event_params(params: dict) -> dict:
    """Strip keys not in ALLOWED_PARAMS and truncate values to 100 chars."""
    if not isinstance(params, dict):
        return {}
    return {k: str(v)[:100] for k, v in params.items() if k in ALLOWED_PARAMS}


def get_period_band(years: int) -> str:
    """Return period band label for analytics."""
    try:
        years = int(years)
    except (ValueError, TypeError):
        return "unknown"
    if years <= 1:
        return "1y"
    elif years <= 3:
        return "1-3y"
    elif years <= 5:
        return "3-5y"
    elif years <= 10:
        return "5-10y"
    else:
        return "10y+"


def get_target_band(amount: float) -> str:
    """Return target amount band label for analytics."""
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return "unknown"
    if amount < 500000:
        return "<500k"
    elif amount < 2000000:
        return "500k-2m"
    elif amount < 10000000:
        return "2m-10m"
    elif amount < 50000000:
        return "10m-50m"
    else:
        return "50m+"


def get_country_band(country: str) -> str:
    """Return country band for analytics."""
    if not country:
        return "unknown"
    country_lower = str(country).lower().strip()
    east_africa = {"kenya", "tanzania", "rwanda", "burundi", "south sudan", "drc", "ethiopia"}
    if country_lower in ("uganda", "ug"):
        return "uganda"
    elif country_lower in east_africa:
        return "east_africa"
    elif country_lower:
        return "diaspora"
    return "unknown"
