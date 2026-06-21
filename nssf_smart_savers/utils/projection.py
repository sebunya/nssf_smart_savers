"""
SmartLife Flexi - Savings Projection Calculator
Demo environment - indicative figures only
"""

FREQUENCY_MAP = {
    "daily": 365,
    "weekly": 52,
    "monthly": 12,
    "quarterly": 4,
    "semi-annually": 2,
    "annually": 1,
}

FREQUENCY_LABELS = {
    "daily": "Daily",
    "weekly": "Weekly",
    "monthly": "Monthly",
    "quarterly": "Quarterly",
    "semi-annually": "Semi-Annually",
    "annually": "Annually",
}

MINIMUM_AMOUNT = 5000  # UGX


def calculate_projection(initial_deposit, periodic_contribution, frequency, years, annual_rate=0.10):
    """
    Calculate savings projection using compound interest with periodic contributions.
    FV = PV*(1+r/n)^(n*t) + PMT * [((1+r/n)^(n*t) - 1) / (r/n)]
    Returns dict with projection data. Indicative for demo purposes only.
    """
    try:
        pv = float(initial_deposit)
        pmt = float(periodic_contribution)
        t = float(years)
        r = float(annual_rate)
        frequency = str(frequency).lower().strip()
    except (ValueError, TypeError):
        return {
            "error": "Invalid input values",
            "total_contributions": 0,
            "projected_value": 0,
            "indicative_return": 0,
            "monthly_data": [],
            "frequency_label": "Monthly",
            "periods_per_year": 12,
        }

    n = FREQUENCY_MAP.get(frequency, 12)
    total_periods = int(n * t)
    r_per_period = r / n if n > 0 else 0

    fv_initial = pv * ((1 + r_per_period) ** total_periods)

    if r_per_period > 0:
        fv_contributions = pmt * (((1 + r_per_period) ** total_periods - 1) / r_per_period)
    else:
        fv_contributions = pmt * total_periods

    projected_value = fv_initial + fv_contributions
    total_contributions = pv + (pmt * total_periods)
    indicative_return = projected_value - total_contributions

    monthly_data = []
    months_to_show = min(int(t * 12), 24)
    monthly_rate = r / 12
    contributions_per_month = n / 12

    balance = pv
    for month in range(1, months_to_show + 1):
        balance = balance * (1 + monthly_rate) + (pmt * contributions_per_month)
        monthly_data.append({"month": month, "balance": round(balance, 2)})

    return {
        "total_contributions": round(total_contributions, 2),
        "projected_value": round(projected_value, 2),
        "indicative_return": round(indicative_return, 2),
        "monthly_data": monthly_data,
        "frequency_label": FREQUENCY_LABELS.get(frequency, "Monthly"),
        "periods_per_year": n,
        "demo_notice": "Projection is indicative for demo purposes only. Actual returns may vary.",
    }


def format_ugx(amount):
    """Format amount as UGX string."""
    try:
        amount = float(amount)
        return "UGX {:,.0f}".format(amount)
    except (ValueError, TypeError):
        return "UGX 0"


def get_frequency_label(frequency):
    """Return human-readable label for frequency."""
    return FREQUENCY_LABELS.get(str(frequency).lower().strip(), frequency)


def validate_minimum(amount, frequency):
    """Validate that amount meets minimum UGX 5,000."""
    try:
        return float(amount) >= MINIMUM_AMOUNT
    except (ValueError, TypeError):
        return False
