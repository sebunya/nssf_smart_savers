#!/usr/bin/env bash
# SmartLife Flexi — Phase 2 smoke test
# Checks: staff queue route, lead scoring module, APIs, PII safety.
# Run after Phase 1 smoke test passes.
set -euo pipefail

BASE="${SMOKE_BASE:-https://nssf-smartlifeflexi.nile-gov-demo.com}"
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PASS=0; FAIL=0; WARN=0

ok()   { echo "[PASS] $1"; PASS=$((PASS+1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL+1)); }
warn() { echo "[WARN] $1"; WARN=$((WARN+1)); }

TMPDIR_P2="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_P2"' EXIT

fetch_page() {
  local route="$1"
  local slug; slug="$(echo "$route" | tr '/' '_')"
  local outfile="$TMPDIR_P2/${slug}.html"
  curl -sSL --max-time 25 \
    --header "Cache-Control: no-cache, no-store" \
    --header "Pragma: no-cache" \
    "$BASE$route?v=p2smoke-$(date +%s)-$RANDOM" \
    -o "$outfile" 2>/dev/null
  printf "%s" "$outfile"
}

contains_file() {
  local file="$1" pattern="$2" label="$3"
  if grep -Eiq "$pattern" "$file" 2>/dev/null; then
    ok "$label"
  else
    fail "$label"
    echo "       Diagnostic (first 15 matching lines):"
    grep -Ein "SmartLife|sl-brand|sl-queue|staff|lead|prototype|NSSF" "$file" 2>/dev/null | head -15 || echo "       (none)"
  fi
}

http_ok() {
  local route="$1"
  local code
  code=$(curl -ksS -o /dev/null -w "%{http_code}" \
    --max-time 20 \
    --header "Cache-Control: no-cache" \
    "$BASE$route?v=p2http-$(date +%s)" 2>/dev/null)
  if [ "$code" = "200" ]; then
    ok "HTTP 200 $route"
  else
    fail "HTTP $code (expected 200) $route"
  fi
}

echo "========================================"
echo "SmartLife Flexi — Phase 2 Smoke Test"
echo "BASE: $BASE"
echo "APP:  $APP_ROOT"
echo "========================================"
echo ""

# ── 1. Phase 1 smoke test baseline ─────────────────────────────────────────
echo "--- Phase 1 baseline ---"
if bash -n "$APP_ROOT/scripts/smoke_test.sh" 2>/dev/null; then
  ok "Phase 1 smoke test syntax valid"
else
  fail "Phase 1 smoke test has syntax errors"
fi

# ── 2. Source: lead scoring module ─────────────────────────────────────────
echo ""
echo "--- Lead scoring module ---"
SCORING_PY="$APP_ROOT/nssf_smart_savers/lead_scoring.py"
if [ -f "$SCORING_PY" ]; then
  ok "lead_scoring.py exists"
else
  fail "lead_scoring.py MISSING"
fi

if grep -q "def calculate_lead_score" "$SCORING_PY" 2>/dev/null; then
  ok "calculate_lead_score function defined"
else
  fail "calculate_lead_score not found in lead_scoring.py"
fi

if grep -q "lead_temperature" "$SCORING_PY" 2>/dev/null; then
  ok "lead_temperature returned by scoring"
else
  fail "lead_temperature not found in scoring output"
fi

if grep -q "next_best_action" "$SCORING_PY" 2>/dev/null; then
  ok "next_best_action returned by scoring"
else
  fail "next_best_action not found in scoring output"
fi

if python3 -c "
import sys
sys.path.insert(0, '$APP_ROOT')
# Minimal standalone check — does the function return expected keys?
import importlib.util, types
spec = importlib.util.spec_from_file_location('lead_scoring', '$SCORING_PY')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
result = m.calculate_lead_score({
    'consent_to_contact': 1,
    'initial_deposit': 200000,
    'frequency': 'monthly',
    'segment': 'new_saver',
    'projection_viewed': 1,
    'checkout_started': 0,
    'payment_completed': 0,
    'preferred_contact_channel': 'sms',
    'age_band': '25-34',
    'goal': 'education',
    'target_amount': 5000000,
    'staff_assisted': 0,
})
assert 'lead_score' in result
assert 'lead_temperature' in result
assert 'next_best_action' in result
assert 'score_reasons' in result
assert isinstance(result['lead_score'], int)
assert result['lead_temperature'] in ('Hot', 'Warm', 'Cold')
assert len(result['score_reasons']) > 0
print('OK score=' + str(result['lead_score']) + ' temp=' + result['lead_temperature'])
" 2>&1; then
  ok "calculate_lead_score returns correct structure"
else
  fail "calculate_lead_score unit test failed"
fi

if python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('lead_scoring', '$SCORING_PY')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
result = m.calculate_lead_score({'consent_to_contact': 0})
assert result['lead_score'] == 0
assert result['lead_temperature'] == 'Cold'
assert 'consent' in result['next_best_action'].lower()
" 2>/dev/null; then
  ok "No-consent lead scores 0 and blocks action"
else
  fail "No-consent guard in scoring is not working"
fi

# ── 3. Source: Phase 2 DocType fields ──────────────────────────────────────
echo ""
echo "--- DocType lifecycle fields ---"
LEAD_JSON="$APP_ROOT/nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json"

for field in lead_status lead_temperature lead_score next_best_action assigned_staff \
             last_contacted_on next_follow_up_on follow_up_outcome drop_off_reason \
             source_route campaign_source campaign_medium campaign_name \
             projection_viewed checkout_started payment_completed; do
  if grep -q "\"$field\"" "$LEAD_JSON" 2>/dev/null; then
    ok "DocType field: $field"
  else
    fail "DocType field MISSING: $field"
  fi
done

# ── 4. Source: Phase 2 APIs ────────────────────────────────────────────────
echo ""
echo "--- Phase 2 API methods ---"
API_PY="$APP_ROOT/nssf_smart_savers/api.py"
for fn in get_lead_summary get_staff_queue update_follow_up_status assign_lead update_journey_flag score_lead; do
  if grep -q "def $fn" "$API_PY" 2>/dev/null; then
    ok "API: $fn defined"
  else
    fail "API: $fn NOT FOUND"
  fi
done

# ── 5. Source: Staff queue route ───────────────────────────────────────────
echo ""
echo "--- Staff queue route ---"
SQ_HTML="$APP_ROOT/nssf_smart_savers/www/smartlife-staff-queue.html"
SQ_PY="$APP_ROOT/nssf_smart_savers/www/smartlife-staff-queue.py"

[ -f "$SQ_HTML" ] && ok "smartlife-staff-queue.html exists" || fail "smartlife-staff-queue.html MISSING"
[ -f "$SQ_PY"   ] && ok "smartlife-staff-queue.py exists"  || fail "smartlife-staff-queue.py MISSING"

if [ -f "$SQ_HTML" ]; then
  grep -q "SmartLife Staff Queue"   "$SQ_HTML" && ok "Staff queue: 'SmartLife Staff Queue' in source"    || fail "Staff queue: 'SmartLife Staff Queue' not in source"
  grep -q "Lead Overview"           "$SQ_HTML" && ok "Staff queue: 'Lead Overview' in source"            || fail "Staff queue: 'Lead Overview' not in source"
  grep -q "Follow-up Priorities"    "$SQ_HTML" && ok "Staff queue: 'Follow-up Priorities' in source"     || fail "Staff queue: 'Follow-up Priorities' not in source"
  grep -q "Lead Temperature"        "$SQ_HTML" && ok "Staff queue: 'Lead Temperature' in source"         || fail "Staff queue: 'Lead Temperature' not in source"
  grep -q "Next Best Actions"       "$SQ_HTML" && ok "Staff queue: 'Next Best Actions' in source"        || fail "Staff queue: 'Next Best Actions' not in source"
  grep -q "Prototype environment"   "$SQ_HTML" && ok "Staff queue: 'Prototype environment' in source"    || fail "Staff queue: 'Prototype environment' not in source"
  grep -q "sl-brand-shell"          "$SQ_HTML" && ok "Staff queue: brand shell wrapper present"          || fail "Staff queue: brand shell wrapper MISSING"
  grep -q "get_lead_summary"        "$SQ_HTML" && ok "Staff queue: calls get_lead_summary"               || fail "Staff queue: get_lead_summary call not found"
  grep -q "get_staff_queue"         "$SQ_HTML" && ok "Staff queue: calls get_staff_queue"                || fail "Staff queue: get_staff_queue call not found"
fi

# ── 6. Python syntax ───────────────────────────────────────────────────────
echo ""
echo "--- Python syntax ---"
if python3 -m py_compile "$APP_ROOT/nssf_smart_savers/lead_scoring.py" 2>/dev/null; then
  ok "lead_scoring.py compiles cleanly"
else
  fail "lead_scoring.py has syntax errors"
fi
if python3 -m py_compile "$APP_ROOT/nssf_smart_savers/api.py" 2>/dev/null; then
  ok "api.py compiles cleanly"
else
  fail "api.py has syntax errors"
fi

# ── 7. PII safety ─────────────────────────────────────────────────────────
echo ""
echo "--- PII safety ---"
# No real PII committed
for pattern in "256[0-9]\{9\}" "0[7][0-9]\{8\}" "@gmail\|@yahoo\|@hotmail" "CM[0-9]\{7\}" "SL-TEST-REAL"; do
  if grep -rq "$pattern" "$APP_ROOT/nssf_smart_savers/www/" "$APP_ROOT/nssf_smart_savers/api.py" \
     "$APP_ROOT/nssf_smart_savers/lead_scoring.py" 2>/dev/null; then
    fail "Potential PII pattern found in source: $pattern"
  else
    ok "No PII pattern: $pattern"
  fi
done

# Phase 2 APIs do not return PII fields directly
if grep -q "first_name\|last_name\|primary_phone\|email_address\|date_of_birth" \
   <(grep -A5 "def get_staff_queue" "$APP_ROOT/nssf_smart_savers/api.py" | grep "return\|\"name\"\|'name'") 2>/dev/null; then
  warn "get_staff_queue may return raw PII field — verify masking is applied"
else
  ok "get_staff_queue does not directly return unmasked PII fields"
fi

# masked fields present
if grep -q "_mask_phone\|_mask_email\|phone_masked\|email_masked" "$API_PY" 2>/dev/null; then
  ok "Phone and email masking present in API"
else
  fail "Phone/email masking NOT found in API"
fi

# ── 8. No credentials committed ───────────────────────────────────────────
echo ""
echo "--- Credential safety ---"
for pattern in "sk_live\|pk_live\|api_key.*=.*['\"][A-Za-z0-9]\{20,\}\|password.*=.*['\"][A-Za-z0-9]\|SECRET_KEY\|PRIVATE_KEY"; do
  if grep -rEq "$pattern" "$APP_ROOT/nssf_smart_savers/" 2>/dev/null; then
    fail "Potential credential in source: $pattern"
  else
    ok "No credential pattern: $pattern"
  fi
done

# ── 9. Live route checks ───────────────────────────────────────────────────
echo ""
echo "--- Live route checks ---"
SQ_FILE="$(fetch_page /smartlife-staff-queue)"
http_ok "/smartlife-staff-queue"

if [ -f "$SQ_FILE" ] && [ -s "$SQ_FILE" ]; then
  contains_file "$SQ_FILE" "SmartLife Staff Queue"    "Rendered: SmartLife Staff Queue heading"
  contains_file "$SQ_FILE" "Lead Overview"            "Rendered: Lead Overview section"
  contains_file "$SQ_FILE" "Follow-up Priorities"     "Rendered: Follow-up Priorities section"
  contains_file "$SQ_FILE" "Lead Temperature"         "Rendered: Lead Temperature section"
  contains_file "$SQ_FILE" "Next Best Actions"        "Rendered: Next Best Actions section"
  contains_file "$SQ_FILE" "Prototype environment"    "Rendered: Prototype environment notice"
  contains_file "$SQ_FILE" "sl-brand-shell|sl-brand-bar" "Rendered: NSSF brand shell"
  contains_file "$SQ_FILE" 'data-brand-title="NSSF SmartLife Flexi"|aria-label="NSSF SmartLife Flexi"' \
    "Rendered: brand title attribute"
  contains_file "$SQ_FILE" "smartlife\.css"           "Rendered: smartlife.css loaded"
else
  warn "Could not fetch /smartlife-staff-queue — skipping rendered checks (run on server)"
fi

# Phase 1 routes still return content
for ROUTE in /smartlife-flexi-demo /smartlife-self-serve /smartlife-staff-assist \
             /smartlife-projection-demo /smartlife-checkout-demo \
             /smartlife-thank-you /smartlife-support-demo; do
  http_ok "$ROUTE"
done

# ── 10. Summary ───────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo "Phase 2 Results: $PASS passed | $FAIL failed | $WARN warnings"
if [ "$FAIL" -eq 0 ]; then
  echo "ALL PHASE 2 CHECKS PASSED"
  exit 0
else
  echo "PHASE 2 HAS FAILURES — review above"
  exit 1
fi
