#!/usr/bin/env bash
# SmartLife Flexi — Phase 2 smoke test (including Personalisation Team access model)
# Checks: lead scoring, DocType fields, access model, PII masking, route content.
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
    echo "       Diagnostic:"
    grep -Ein "SmartLife|sl-brand|sl-queue|staff|lead|prototype|NSSF|authorised|sign-in" \
      "$file" 2>/dev/null | head -12 || echo "       (none)"
  fi
}

NETWORK_AVAILABLE=""
_check_network() {
  if [ -z "${BASE:-}" ]; then
    NETWORK_AVAILABLE="no"
    return 0
  fi

  local tmp_file
  tmp_file="$(mktemp)"

  if curl -ksS --max-time 8 "$BASE/" -o "$tmp_file" >/dev/null 2>&1; then
    if [ -s "$tmp_file" ]; then
      NETWORK_AVAILABLE="yes"
    else
      NETWORK_AVAILABLE="no"
    fi
  else
    NETWORK_AVAILABLE="no"
  fi

  rm -f "$tmp_file"
  return 0
}

http_ok() {
  local route="$1"
  _check_network
  if [ "$NETWORK_AVAILABLE" = "no" ]; then
    warn "NETWORK UNAVAILABLE — live check skipped (run on server): HTTP 200 $route"
    return
  fi
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

API_PY="$APP_ROOT/nssf_smart_savers/api.py"
SCORING_PY="$APP_ROOT/nssf_smart_savers/lead_scoring.py"
LEAD_JSON="$APP_ROOT/nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json"
ANALYTICS_PY="$APP_ROOT/nssf_smart_savers/utils/analytics.py"
SQ_HTML="$APP_ROOT/nssf_smart_savers/www/smartlife-staff-queue.html"
SQF_HTML="$APP_ROOT/nssf_smart_savers/www/smartlife-staff-queue-full.html"
SQF_PY="$APP_ROOT/nssf_smart_savers/www/smartlife-staff-queue-full.py"

echo "========================================"
echo "SmartLife Flexi — Phase 2 Smoke Test"
echo "BASE: $BASE"
echo "APP:  $APP_ROOT"
echo "========================================"
echo ""

# ── 1. Phase 1 baseline ────────────────────────────────────────────
echo "--- Phase 1 baseline ---"
bash -n "$APP_ROOT/scripts/smoke_test.sh" 2>/dev/null \
  && ok "Phase 1 smoke test syntax valid" \
  || fail "Phase 1 smoke test has syntax errors"

# ── 2. Lead scoring module ─────────────────────────────────────────
echo ""
echo "--- Lead scoring module ---"
[ -f "$SCORING_PY" ] && ok "lead_scoring.py exists" || fail "lead_scoring.py MISSING"
grep -q "def calculate_lead_score" "$SCORING_PY" 2>/dev/null \
  && ok "calculate_lead_score defined" || fail "calculate_lead_score not found"

python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('lead_scoring', '$SCORING_PY')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.calculate_lead_score({
    'consent_to_contact': 1, 'initial_deposit': 200000, 'frequency': 'monthly',
    'segment': 'new_saver', 'projection_viewed': 1, 'checkout_started': 0,
    'payment_completed': 0, 'preferred_contact_channel': 'sms',
    'age_band': '25-34', 'goal': 'education', 'target_amount': 5000000,
})
assert 'lead_score' in r and 'lead_temperature' in r and 'next_best_action' in r
assert isinstance(r['lead_score'], int) and r['lead_temperature'] in ('Hot','Warm','Cold')
" 2>/dev/null && ok "calculate_lead_score unit test passes" || fail "calculate_lead_score unit test failed"

python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('lead_scoring', '$SCORING_PY')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.calculate_lead_score({'consent_to_contact': 0})
assert r['lead_score'] == 0 and r['lead_temperature'] == 'Cold'
" 2>/dev/null && ok "No-consent → score=0, temp=Cold" || fail "No-consent guard broken"

# ── 3. DocType lifecycle fields ────────────────────────────────────
echo ""
echo "--- DocType lifecycle fields ---"
for field in lead_status lead_temperature lead_score next_best_action assigned_staff \
             last_contacted_on next_follow_up_on follow_up_outcome drop_off_reason \
             source_route campaign_source campaign_medium campaign_name \
             projection_viewed checkout_started payment_completed staff_notes; do
  grep -q "\"$field\"" "$LEAD_JSON" 2>/dev/null \
    && ok "DocType field: $field" || fail "DocType field MISSING: $field"
done

# ── 4. Auth helpers and role constants ────────────────────────────
echo ""
echo "--- Auth helpers and role guard ---"
grep -q "def _is_guest" "$API_PY" 2>/dev/null \
  && ok "_is_guest() defined" || fail "_is_guest() not found"
grep -q "def _require_authenticated_staff" "$API_PY" 2>/dev/null \
  && ok "_require_authenticated_staff() defined" || fail "_require_authenticated_staff() not found"
grep -q "def _require_personalisation_access" "$API_PY" 2>/dev/null \
  && ok "_require_personalisation_access() defined" || fail "_require_personalisation_access() not found"
grep -q "def _has_allowed_personalisation_role" "$API_PY" 2>/dev/null \
  && ok "_has_allowed_personalisation_role() defined" || fail "_has_allowed_personalisation_role() not found"
grep -q "ALLOWED_PERSONALISATION_ROLES" "$API_PY" 2>/dev/null \
  && ok "ALLOWED_PERSONALISATION_ROLES constant defined" || fail "ALLOWED_PERSONALISATION_ROLES not found"
grep -q '"SmartLife Personalisation Team"' "$API_PY" 2>/dev/null \
  && ok "Role: 'SmartLife Personalisation Team' in role set" || fail "'SmartLife Personalisation Team' NOT in role set"
grep -q '"NSSF Staff"' "$API_PY" 2>/dev/null \
  && ok "Role: 'NSSF Staff' in role set" || fail "'NSSF Staff' NOT in role set"
grep -q '"System Manager"' "$API_PY" 2>/dev/null \
  && ok "Role: 'System Manager' in role set" || fail "'System Manager' NOT in role set"
grep -q "frappe.get_roles" "$API_PY" 2>/dev/null \
  && ok "_require_personalisation_access uses frappe.get_roles" || fail "frappe.get_roles NOT found in api.py"
# _require_personalisation_access must actually call the role helper
python3 -c "
import re, sys
src = open('$API_PY').read()
m = re.search(r'def _require_personalisation_access\b.*?(?=\ndef |\Z)', src, re.DOTALL)
if m and '_has_allowed_personalisation_role' in m.group():
    sys.exit(0)
sys.exit(1)
" 2>/dev/null \
  && ok "_require_personalisation_access calls _has_allowed_personalisation_role" \
  || fail "_require_personalisation_access does NOT call _has_allowed_personalisation_role"

# ── 5. Public guest-safe endpoints (may be allow_guest) ───────────
echo ""
echo "--- Guest-safe endpoints (aggregated/masked only) ---"
for fn in get_lead_summary get_staff_queue; do
  grep -q "def $fn" "$API_PY" 2>/dev/null \
    && ok "API: $fn defined" || fail "API: $fn NOT FOUND"
done
# Confirm get_staff_queue still uses masking
grep -q "_mask_phone\|phone_masked\|email_masked" "$API_PY" 2>/dev/null \
  && ok "get_staff_queue: masking helpers present" || fail "get_staff_queue: masking helpers MISSING"

# ── 6. Authenticated full-PII endpoints: NOT allow_guest ──────────
echo ""
echo "--- Authenticated full-PII endpoints ---"
for fn in get_staff_queue_full get_lead_full_detail; do
  grep -q "def $fn" "$API_PY" 2>/dev/null \
    && ok "API: $fn defined" || fail "API: $fn NOT FOUND"
  # Must NOT have allow_guest=True
  # Exit code 1 = NOT guest-allowed (good); exit 0 = guest allowed (bad)
  python3 -c "
import ast, sys
src = open('$API_PY').read()
tree = ast.parse(src)
found = False
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == '$fn':
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call):
                for kw in deco.keywords:
                    if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value:
                        found = True
sys.exit(0 if found else 1)
" 2>/dev/null \
    && fail "$fn: allow_guest=True found — must be authenticated only" \
    || ok "$fn: not allow_guest (authenticated required)"
  # Must call personalisation access guard (search lines between def and next top-level def)
  python3 -c "
import re, sys
src = open('$API_PY').read()
m = re.search(r'def $fn\b.*?(?=\ndef |\Z)', src, re.DOTALL)
if m and '_require_personalisation_access' in m.group():
    sys.exit(0)
sys.exit(1)
" 2>/dev/null \
    && ok "$fn: calls _require_personalisation_access" \
    || fail "$fn: _require_personalisation_access NOT called"
done

# ── 7. Write endpoints: NOT allow_guest, call auth guard ──────────
echo ""
echo "--- Write endpoint protection ---"
for fn in update_follow_up_status assign_lead update_journey_flag; do
  grep -q "def $fn" "$API_PY" 2>/dev/null \
    && ok "API: $fn defined" || fail "API: $fn NOT FOUND"
  python3 -c "
import ast, sys
src = open('$API_PY').read()
tree = ast.parse(src)
found = False
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == '$fn':
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call):
                for kw in deco.keywords:
                    if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value:
                        found = True
sys.exit(0 if found else 1)
" 2>/dev/null \
    && fail "$fn: allow_guest=True — write endpoint must not allow guest" \
    || ok "$fn: not allow_guest (write protected)"
  python3 -c "
import re, sys
src = open('$API_PY').read()
m = re.search(r'def $fn\b.*?(?=\ndef |\Z)', src, re.DOTALL)
if m and ('_require_authenticated_staff' in m.group() or '_require_personalisation_access' in m.group()):
    sys.exit(0)
sys.exit(1)
" 2>/dev/null \
    && ok "$fn: calls auth guard" || fail "$fn: auth guard NOT found"
done

# ── 8. Public staff queue page ─────────────────────────────────────
echo ""
echo "--- Public staff queue (masked demo view) ---"
[ -f "$SQ_HTML" ] && ok "smartlife-staff-queue.html exists" || fail "MISSING"
if [ -f "$SQ_HTML" ]; then
  grep -q "SmartLife Staff Queue"  "$SQ_HTML" && ok "Masked queue: 'SmartLife Staff Queue' present" || fail "MISSING"
  grep -q "Masked demo view"        "$SQ_HTML" && ok "Masked queue: 'Masked demo view' label present" || fail "'Masked demo view' MISSING"
  grep -q "Lead Overview"           "$SQ_HTML" && ok "Masked queue: 'Lead Overview' present"  || fail "MISSING"
  grep -q "Follow-up Priorities"    "$SQ_HTML" && ok "Masked queue: 'Follow-up Priorities'"   || fail "MISSING"
  grep -q "Lead Temperature"        "$SQ_HTML" && ok "Masked queue: 'Lead Temperature'"       || fail "MISSING"
  grep -q "Next Best Actions"       "$SQ_HTML" && ok "Masked queue: 'Next Best Actions'"      || fail "MISSING"
  grep -q "Prototype environment"   "$SQ_HTML" && ok "Masked queue: 'Prototype environment'"  || fail "MISSING"
  # Must NOT contain raw PII rendering patterns in HTML source
  if grep -q 'l\.primary_phone[^_]' "$SQ_HTML" 2>/dev/null; then
    fail "Masked queue source renders l.primary_phone (unmasked) — use phone_masked"
  else
    ok "Masked queue: no unmasked primary_phone in source template"
  fi
fi

# ── 9. Authenticated full-PII staff queue page ────────────────────
echo ""
echo "--- Authenticated full-PII view ---"
[ -f "$SQF_HTML" ] && ok "smartlife-staff-queue-full.html exists" || fail "MISSING"
[ -f "$SQF_PY"   ] && ok "smartlife-staff-queue-full.py exists"   || fail "MISSING"
if [ -f "$SQF_HTML" ]; then
  grep -q "SmartLife Personalisation Team"    "$SQF_HTML" && ok "Full view: 'SmartLife Personalisation Team'" || fail "MISSING"
  grep -q "Full Lead Details"                 "$SQF_HTML" && ok "Full view: 'Full Lead Details'"              || fail "MISSING"
  grep -q "Internal authorised view"          "$SQF_HTML" && ok "Full view: 'Internal authorised view'"       || fail "MISSING"
  grep -q "PII access enabled for authorised" "$SQF_HTML" && ok "Full view: 'PII access enabled...'"          || fail "MISSING"
  grep -q "Staff sign-in required"            "$SQF_HTML" && ok "Full view: 'Staff sign-in required'"         || fail "MISSING"
  grep -q "Follow-up Actions"                 "$SQF_HTML" && ok "Full view: 'Follow-up Actions'"              || fail "MISSING"
  grep -q "Consent Status"                    "$SQF_HTML" && ok "Full view: 'Consent Status'"                 || fail "MISSING"
  grep -q "Next Best Action"                  "$SQF_HTML" && ok "Full view: 'Next Best Action'"               || fail "MISSING"
  grep -q "get_staff_queue_full"              "$SQF_HTML" && ok "Full view: calls get_staff_queue_full"       || fail "MISSING"
  grep -q "sl-brand-shell"                    "$SQF_HTML" && ok "Full view: NSSF brand shell present"         || fail "MISSING"
fi

# ── 10. Analytics PII block list ──────────────────────────────────
echo ""
echo "--- Analytics PII block list (server) ---"
# Check PII keys appear in server-side analytics.py comment/guard (instructs the deny list)
for key in first_name last_name full_name phone primary_phone email nin date_of_birth \
           birthday_day birthday_month age_years notes remarks raw_remarks \
           user_submitted_text; do
  # Accept the key appearing in comments OR in the ALLOWED_PARAMS deny-list comment
  if grep -q "$key" "$ANALYTICS_PY" 2>/dev/null; then
    ok "Analytics server: '$key' referenced in analytics.py"
  elif grep -q "'$key'" "$APP_ROOT/nssf_smart_savers/public/js/analytics_helper.js" 2>/dev/null; then
    ok "Analytics JS: '$key' in analytics_helper.js"
  else
    warn "Analytics: '$key' not explicitly named in analytics files (blocked by allowlist architecture)"
  fi
done

# Confirm ALLOWED_PARAMS does NOT include PII keys
# Uses ast.Constant.value (not deprecated .s) — compatible with Python 3.8+/3.12+
python3 -c "
import ast, sys

ANALYTICS_PY = '$ANALYTICS_PY'
src = open(ANALYTICS_PY).read()
tree = ast.parse(src)

allowed = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'ALLOWED_PARAMS':
                allowed = [
                    e.value for e in node.value.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)
                ]

PII_KEYS = {
    'first_name', 'last_name', 'full_name', 'phone', 'primary_phone',
    'email', 'nin', 'national_id', 'date_of_birth', 'dob',
    'birthday_day', 'birthday_month', 'age_years', 'exact_age',
    'staff_notes', 'notes', 'remarks', 'raw_remarks',
    'user_submitted_text', 'free_text',
}

bad = PII_KEYS.intersection(set(allowed))
if bad:
    print('FAIL: PII keys in ALLOWED_PARAMS: ' + ', '.join(sorted(bad)))
    sys.exit(1)

print('PASS: ALLOWED_PARAMS contains no PII keys (' + str(len(allowed)) + ' safe params)')
sys.exit(0)
" 2>&1 | while IFS= read -r line; do
  if echo "$line" | grep -q '^PASS:'; then
    ok "Analytics ALLOWED_PARAMS: ${line#PASS: }"
  elif echo "$line" | grep -q '^FAIL:'; then
    fail "Analytics ALLOWED_PARAMS: ${line#FAIL: }"
  fi
done

# Frontend JS analytics block list
JS_FILE="$APP_ROOT/nssf_smart_savers/public/js/analytics_helper.js"
[ -f "$JS_FILE" ] && ok "analytics_helper.js exists" || fail "analytics_helper.js MISSING"
for key in first_name last_name primary_phone birthday_day birthday_month age_years nin; do
  grep -q "'$key'" "$JS_FILE" 2>/dev/null \
    && ok "JS analytics: '$key' in PII_KEYS block list" \
    || fail "JS analytics: '$key' NOT in PII_KEYS block list"
done

# ── 11. Python syntax ──────────────────────────────────────────────
echo ""
echo "--- Python syntax ---"
python3 -m py_compile "$SCORING_PY" 2>/dev/null && ok "lead_scoring.py compiles" || fail "lead_scoring.py syntax error"
python3 -m py_compile "$API_PY"     2>/dev/null && ok "api.py compiles"           || fail "api.py syntax error"
python3 -m py_compile "$APP_ROOT/nssf_smart_savers/utils/analytics.py" 2>/dev/null \
  && ok "analytics.py compiles" || fail "analytics.py syntax error"
python3 -m py_compile "$SQF_PY" 2>/dev/null \
  && ok "smartlife-staff-queue-full.py compiles" || fail "smartlife-staff-queue-full.py syntax error"

# ── 12. No credentials in source ──────────────────────────────────
echo ""
echo "--- Credential safety ---"
if grep -rEq "sk_live|pk_live|SECRET_KEY|PRIVATE_KEY" \
   "$APP_ROOT/nssf_smart_savers/" 2>/dev/null; then
  fail "Potential credential pattern found in source"
else
  ok "No credential patterns in source"
fi

# ── 13. Live route checks ──────────────────────────────────────────
# NOTE: HTTP 200 checks require merge into production branch AND bench migrate
# (staff_notes column + any other Phase 2 DocType additions).
# HTTP 417 on Phase 2 routes after branch deploy indicates bench migrate is pending.
# Source code checks above are authoritative for CI. Run on server after migrate.
echo ""
echo "--- Live route checks ---"
_check_network
SQ_FILE="$(fetch_page /smartlife-staff-queue)"
SQF_FILE="$(fetch_page /smartlife-staff-queue-full)"

http_ok "/smartlife-staff-queue"
http_ok "/smartlife-staff-queue-full"

if [ "$NETWORK_AVAILABLE" = "no" ]; then
  warn "NETWORK UNAVAILABLE — rendered content checks skipped (requires deployed server + bench migrate)"
elif [ -f "$SQ_FILE" ] && [ -s "$SQ_FILE" ]; then
  contains_file "$SQ_FILE" "SmartLife Staff Queue"  "Rendered: masked queue heading"
  contains_file "$SQ_FILE" "Masked demo view"        "Rendered: masked demo view notice"
  contains_file "$SQ_FILE" "Prototype environment"   "Rendered: prototype notice"
else
  warn "Could not fetch /smartlife-staff-queue — skipping rendered checks (requires deployed server + bench migrate)"
fi

if [ "$NETWORK_AVAILABLE" != "no" ] && [ -f "$SQF_FILE" ] && [ -s "$SQF_FILE" ]; then
  contains_file "$SQF_FILE" "SmartLife Personalisation Team" "Rendered: full view heading"
  contains_file "$SQF_FILE" "Staff sign-in required|Access restricted|Full Lead Details|Internal authorised view" \
    "Rendered: full view gate or content"
elif [ "$NETWORK_AVAILABLE" != "no" ]; then
  warn "Could not fetch /smartlife-staff-queue-full — skipping rendered checks (requires deployed server + bench migrate)"
fi

# Phase 1 routes still up (skipped automatically if network unavailable)
for ROUTE in /smartlife-flexi-demo /smartlife-self-serve /smartlife-staff-assist \
             /smartlife-projection-demo /smartlife-checkout-demo \
             /smartlife-thank-you /smartlife-support-demo; do
  http_ok "$ROUTE"
done

# ── 14. Summary ────────────────────────────────────────────────────
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
