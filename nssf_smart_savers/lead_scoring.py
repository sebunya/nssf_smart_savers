"""
SmartLife Flexi — Lead scoring engine.
Deterministic, explainable, PII-free.
Returns lead_score (0-100), lead_temperature, next_best_action, score_reasons.
Demo environment only.
"""


def _safe_float(v, default=0.0):
    try:
        return float(v or 0)
    except (ValueError, TypeError):
        return default


def _safe_int(v, default=0):
    try:
        return int(v or 0)
    except (ValueError, TypeError):
        return default


def _safe_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, int):
        return bool(v)
    return str(v).lower() in ("1", "true", "yes")


# ---------------------------------------------------------------------------
# Scoring weights (total max = 100)
# ---------------------------------------------------------------------------

_FREQUENCY_SCORES = {
    "daily":         5,
    "weekly":        4,
    "bi-weekly":     3,
    "monthly":       2,
    "quarterly":     1,
}

_AGE_BAND_SCORES = {
    "25-34": 5,
    "35-44": 5,
    "20-24": 4,
    "45-54": 4,
    "16-19": 3,
    "55+":   3,
}

_SAVER_TYPE_SCORES = {
    "existing_member":         10,
    "new_saver":               8,
    "informal_sector":         7,
    "diaspora":                6,
    "staff_assisted_prospect": 9,
}

_CONTACT_CHANNEL_SCORES = {
    "sms":       5,
    "whatsapp":  5,
    "email":     4,
    "call":      5,
    "phone":     5,
}


def calculate_lead_score(lead_or_dict):
    """
    Score a lead dict or Frappe Document.

    Returns a dict:
      lead_score       int 0-100
      lead_temperature "Hot" | "Warm" | "Cold"
      next_best_action str
      score_reasons    list[str]
    """
    if hasattr(lead_or_dict, "as_dict"):
        d = lead_or_dict.as_dict()
    elif isinstance(lead_or_dict, dict):
        d = lead_or_dict
    else:
        raise TypeError("Expected dict or Frappe Document")

    score = 0
    reasons = []

    # ── Consent (gate) ────────────────────────────────────────────
    consent = _safe_bool(d.get("consent_to_contact", False))
    if not consent:
        return {
            "lead_score": 0,
            "lead_temperature": "Cold",
            "next_best_action": "No action until consent is granted",
            "score_reasons": ["Consent not given — lead is not actionable"],
        }
    score += 15
    reasons.append("+15 consent given")

    # ── Payment completed (highest quality signal) ─────────────────
    if _safe_bool(d.get("payment_completed")):
        score += 30
        reasons.append("+30 payment completed")
    elif _safe_bool(d.get("checkout_started")):
        score += 15
        reasons.append("+15 checkout started")

    # ── Monthly contribution amount ────────────────────────────────
    monthly = _safe_float(d.get("initial_deposit") or d.get("monthly_contribution") or d.get("target_amount", 0))
    if monthly >= 500_000:
        score += 10
        reasons.append("+10 high contribution amount")
    elif monthly >= 100_000:
        score += 7
        reasons.append("+7 medium contribution amount")
    elif monthly >= 50_000:
        score += 4
        reasons.append("+4 modest contribution amount")
    elif monthly > 0:
        score += 2
        reasons.append("+2 some contribution indicated")

    # ── Contribution frequency ─────────────────────────────────────
    freq = str(d.get("frequency") or "").lower()
    freq_score = _FREQUENCY_SCORES.get(freq, 0)
    if freq_score:
        score += freq_score
        reasons.append(f"+{freq_score} frequency={freq}")

    # ── Saver type ─────────────────────────────────────────────────
    saver_type = str(d.get("segment") or d.get("saver_type") or "").lower().replace(" ", "_")
    st_score = _SAVER_TYPE_SCORES.get(saver_type, 3)
    score += st_score
    reasons.append(f"+{st_score} saver_type={saver_type or 'unknown'}")

    # ── Projection viewed ──────────────────────────────────────────
    if _safe_bool(d.get("projection_viewed")):
        score += 8
        reasons.append("+8 projection viewed")

    # ── Staff assisted ─────────────────────────────────────────────
    if _safe_bool(d.get("staff_assisted")):
        score += 5
        reasons.append("+5 staff assisted")

    # ── Preferred contact channel ──────────────────────────────────
    channel = str(d.get("preferred_contact_channel") or "").lower()
    ch_score = _CONTACT_CHANNEL_SCORES.get(channel, 0)
    if ch_score:
        score += ch_score
        reasons.append(f"+{ch_score} contact_channel={channel}")
    else:
        reasons.append("−0 no contact channel (reduces actionability)")

    # ── Age band ──────────────────────────────────────────────────
    age_band = str(d.get("age_band") or "")
    ab_score = _AGE_BAND_SCORES.get(age_band, 2)
    score += ab_score
    reasons.append(f"+{ab_score} age_band={age_band or 'unknown'}")

    # ── Goal clarity ──────────────────────────────────────────────
    if d.get("goal") and d.get("target_amount") and _safe_float(d.get("target_amount")) > 0:
        score += 5
        reasons.append("+5 goal with target amount")
    elif d.get("goal"):
        score += 2
        reasons.append("+2 goal selected")

    # ── Source route ──────────────────────────────────────────────
    source = str(d.get("source_route") or "").lower()
    if "checkout" in source:
        score += 3
        reasons.append("+3 sourced from checkout route")
    elif "self-serve" in source or "self_serve" in source:
        score += 2
        reasons.append("+2 sourced from self-serve route")

    score = min(score, 100)

    # ── Temperature ───────────────────────────────────────────────
    if score >= 65:
        temperature = "Hot"
    elif score >= 35:
        temperature = "Warm"
    else:
        temperature = "Cold"

    # ── Next best action ──────────────────────────────────────────
    payment_done  = _safe_bool(d.get("payment_completed"))
    checkout_done = _safe_bool(d.get("checkout_started"))
    projection_ok = _safe_bool(d.get("projection_viewed"))
    staff_flag    = _safe_bool(d.get("staff_assisted"))

    if payment_done:
        nba = "Mark as converted"
    elif checkout_done:
        nba = "Send initial deposit reminder"
    elif projection_ok:
        nba = "Invite to complete checkout"
    elif temperature == "Hot" and staff_flag:
        nba = "Call within 24 hours"
    elif temperature == "Hot":
        nba = "Send projection reminder"
    elif temperature == "Warm" and staff_flag:
        nba = "Assign to staff"
    elif temperature == "Warm":
        nba = "Send education content"
    else:
        nba = "Send education content"

    return {
        "lead_score":       score,
        "lead_temperature": temperature,
        "next_best_action": nba,
        "score_reasons":    reasons,
    }
