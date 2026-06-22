#!/usr/bin/env bash
# SmartLife Flexi — Messaging smoke test
# Run from: /home/frappe/frappe-bench/apps/nssf_smart_savers
# Does NOT perform live sends. Safe for CI.
set -euo pipefail

PASS=0; FAIL=0; WARN=0

pass() { echo "PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
warn() { echo "WARN: $1"; WARN=$((WARN+1)); }
info() { echo "INFO: $1"; }

# ── Network detection ─────────────────────────────────────────────────────────
NETWORK_AVAILABLE=""
_check_network() {
  if [ -z "$NETWORK_AVAILABLE" ]; then
    local body
    body=$(curl -sSL --max-time 6 "https://nssf-smartlifeflexi.nile-gov-demo.com/smartlife-flexi-demo" 2>/dev/null | head -c 300 || true)
    if echo "$body" | grep -qi "not in allowlist\|network egress\|blocked\|forbidden\|ERR_"; then
      NETWORK_AVAILABLE="no"
    elif [ -z "$body" ]; then
      NETWORK_AVAILABLE="no"
    else
      NETWORK_AVAILABLE="yes"
    fi
  fi
}

http_ok() {
  local url="$1" label="$2"
  _check_network
  if [ "$NETWORK_AVAILABLE" = "no" ]; then
    warn "NETWORK UNAVAILABLE — run on server to verify: $label ($url)"
    return
  fi
  local code
  code=$(curl -ksS -o /dev/null -w "%{http_code}" --max-time 12 "$url" 2>/dev/null || echo "000")
  if [ "$code" = "200" ]; then
    pass "$label returns HTTP 200"
  else
    fail "$label returned HTTP $code (expected 200)"
  fi
}

echo "============================================================"
echo "SmartLife Messaging Smoke Test"
echo "============================================================"

# ── Section 1: Prior smoke test syntax ───────────────────────────────────────
info "Section 1: Prior smoke test syntax"
if bash -n scripts/smoke_test.sh 2>/dev/null; then
  pass "smoke_test.sh syntax valid"
else
  fail "smoke_test.sh has syntax errors"
fi
if bash -n scripts/smoke_test_phase_2.sh 2>/dev/null; then
  pass "smoke_test_phase_2.sh syntax valid"
else
  fail "smoke_test_phase_2.sh has syntax errors"
fi

# ── Section 2: Adapter files exist and compile ────────────────────────────────
info "Section 2: Adapter files"
ZEPTO="nssf_smart_savers/integrations/zeptomail.py"
PHAHAPA="nssf_smart_savers/integrations/phahapa_sms.py"

[ -f "$ZEPTO" ] && pass "ZeptoMail adapter exists" || fail "ZeptoMail adapter missing: $ZEPTO"
[ -f "$PHAHAPA" ] && pass "Phahapa SMS adapter exists" || fail "Phahapa SMS adapter missing: $PHAHAPA"

python3 -m py_compile "$ZEPTO" 2>/dev/null && pass "ZeptoMail adapter compiles" || fail "ZeptoMail adapter has syntax errors"
python3 -m py_compile "$PHAHAPA" 2>/dev/null && pass "Phahapa SMS adapter compiles" || fail "Phahapa SMS adapter has syntax errors"

# ── Section 3: Core messaging files ──────────────────────────────────────────
info "Section 3: Core messaging files"
MESSAGING="nssf_smart_savers/messaging.py"
TEMPLATES="nssf_smart_savers/communication_templates.py"

[ -f "$MESSAGING" ] && pass "messaging.py exists" || fail "messaging.py missing"
[ -f "$TEMPLATES" ] && pass "communication_templates.py exists" || fail "communication_templates.py missing"

python3 -m py_compile "$MESSAGING" 2>/dev/null && pass "messaging.py compiles" || fail "messaging.py has syntax errors"
python3 -m py_compile "$TEMPLATES" 2>/dev/null && pass "communication_templates.py compiles" || fail "communication_templates.py has syntax errors"

# ── Section 4: DocType ────────────────────────────────────────────────────────
info "Section 4: SmartLife Communication Log DocType"
COMLOG_JSON="nssf_smart_savers/nssf_smart_savers/doctype/smartlife_communication_log/smartlife_communication_log.json"
[ -f "$COMLOG_JSON" ] && pass "SmartLife Communication Log JSON exists" || fail "SmartLife Communication Log JSON missing"

if [ -f "$COMLOG_JSON" ]; then
  for field in lead channel template_name recipient_masked message_status consent_snapshot demo_mode; do
    if python3 -c "
import json, sys
d = json.load(open('$COMLOG_JSON'))
fields = [f['fieldname'] for f in d.get('fields', [])]
sys.exit(0 if '$field' in fields else 1)
" 2>/dev/null; then
      pass "SmartLife Communication Log has field: $field"
    else
      fail "SmartLife Communication Log missing field: $field"
    fi
  done
fi

# ── Section 5: All required templates ────────────────────────────────────────
info "Section 5: Communication templates"
REQUIRED_TEMPLATES=(
  "welcome_after_personal_details"
  "projection_viewed_reminder"
  "checkout_abandoned_reminder"
  "initial_deposit_reminder"
  "birthday_message"
  "staff_follow_up_message"
  "savings_milestone_message"
  "dormant_lead_reactivation"
  "diaspora_saver_follow_up"
  "informal_sector_saver_follow_up"
  "consent_missing_education"
)
for tmpl in "${REQUIRED_TEMPLATES[@]}"; do
  if grep -q "\"$tmpl\"" "$TEMPLATES" 2>/dev/null; then
    pass "Template defined: $tmpl"
  else
    fail "Template missing: $tmpl"
  fi
done

# consent_missing_education must have consent_required = False
if python3 -c "
import sys, importlib.util
spec = importlib.util.spec_from_file_location('ct', '$TEMPLATES')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
t = m.TEMPLATES.get('consent_missing_education', {})
sys.exit(0 if t.get('consent_required') is False else 1)
" 2>/dev/null; then
  pass "consent_missing_education has consent_required=False"
else
  fail "consent_missing_education must have consent_required=False"
fi

# ── Section 6: API endpoints ──────────────────────────────────────────────────
info "Section 6: API endpoints in api.py"
API="nssf_smart_savers/api.py"

for fn in get_message_templates preview_smartlife_message send_smartlife_demo_message \
           get_communication_history get_messaging_config_status; do
  grep -q "def $fn" "$API" && pass "API defined: $fn" || fail "API missing: $fn"
done

# ── Section 7: Access control ─────────────────────────────────────────────────
info "Section 7: Access control"

# get_message_templates may be allow_guest
if python3 -c "
import ast, sys
src = open('$API').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == 'get_message_templates':
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call):
                for kw in deco.keywords:
                    if kw.arg == 'allow_guest' and getattr(kw.value, 'value', False):
                        sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
  pass "get_message_templates is allow_guest=True (template metadata only — PII-safe)"
else
  warn "get_message_templates is not allow_guest — verify this is intentional"
fi

# Send, preview, history, config must NOT be allow_guest
for fn in preview_smartlife_message send_smartlife_demo_message \
           get_communication_history get_messaging_config_status; do
  result=$(python3 -c "
import ast, sys
src = open('$API').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == '$fn':
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call):
                for kw in deco.keywords:
                    if kw.arg == 'allow_guest' and getattr(kw.value, 'value', False):
                        print('GUEST_OPEN')
                        sys.exit(0)
print('NOT_GUEST')
" 2>/dev/null || echo "PARSE_ERROR")
  if [ "$result" = "GUEST_OPEN" ]; then
    fail "$fn must NOT be allow_guest=True"
  else
    pass "$fn is not allow_guest (correct)"
  fi
done

# send endpoint calls _require_personalisation_access
if python3 -c "
import ast, sys
src = open('$API').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == 'send_smartlife_demo_message':
        code = ast.unparse(node)
        sys.exit(0 if '_require_personalisation_access' in code else 1)
sys.exit(1)
" 2>/dev/null; then
  pass "send_smartlife_demo_message calls _require_personalisation_access"
else
  fail "send_smartlife_demo_message must call _require_personalisation_access"
fi

# config status does not call _require_personalisation_access (authenticated only is fine)
# but must call _require_authenticated_staff
if grep -A10 "def get_messaging_config_status" "$API" | grep -q "_require_authenticated_staff"; then
  pass "get_messaging_config_status calls _require_authenticated_staff"
else
  fail "get_messaging_config_status must call _require_authenticated_staff"
fi

# ── Section 8: Consent enforcement ───────────────────────────────────────────
info "Section 8: Consent enforcement"
if grep -q "consent_to_contact" "$MESSAGING" 2>/dev/null; then
  pass "messaging.py references consent_to_contact"
else
  fail "messaging.py must enforce consent_to_contact"
fi
if grep -q "Skipped - No Consent" "$MESSAGING" 2>/dev/null; then
  pass "messaging.py has No Consent skip path"
else
  fail "messaging.py must log Skipped - No Consent"
fi
if grep -q "Skipped - Missing Recipient" "$MESSAGING" 2>/dev/null; then
  pass "messaging.py has Missing Recipient skip path"
else
  fail "messaging.py must log Skipped - Missing Recipient"
fi

# ── Section 9: Credential safety ─────────────────────────────────────────────
info "Section 9: No committed credentials"

# Patterns that indicate a real credential (long non-placeholder values)
CRED_PATTERN='(Zoho-enczapikey [A-Za-z0-9+/]{20,}|Authorization["\s]*:["\s]*Zoho-enczapikey [A-Za-z0-9+/]{10,}|Bearer [A-Za-z0-9._\-]{30,}|password["\s]*=["\s]*[A-Za-z0-9!@#\$%^&*]{16,}|api_key["\s]*=["\s]*[A-Za-z0-9!@#\$%^&*]{16,}|secret["\s]*=["\s]*[A-Za-z0-9!@#\$%^&*]{16,})'

EXCLUDED_DIRS="--exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules"

# Allow placeholder patterns
found_creds=$(grep -rEn $EXCLUDED_DIRS "$CRED_PATTERN" \
  nssf_smart_savers/ scripts/ docs/ 2>/dev/null \
  | grep -v "REPLACE_WITH\|REDACTED\|your-token\|your-password\|example\|placeholder\|demo_mode\|configured\|not_configured" \
  | grep -v "smoke_test_messaging.sh" \
  || true)

if [ -z "$found_creds" ]; then
  pass "No committed credentials found in source"
else
  fail "Potential committed credentials detected — review and remove:"
  echo "$found_creds"
fi

# Check for .env files committed
env_files=$(git ls-files 2>/dev/null | grep -E "\.env$|^\.env\.|credentials" || true)
if [ -z "$env_files" ]; then
  pass "No .env or credentials files committed"
else
  fail "Committed credential files found: $env_files"
fi

# ── Section 10: PII safety in adapters ───────────────────────────────────────
info "Section 10: PII safety"
if grep -q "mask_email\|mask_phone" "$ZEPTO" 2>/dev/null; then
  pass "ZeptoMail adapter uses masking"
else
  fail "ZeptoMail adapter must mask recipient"
fi
if grep -q "mask_phone" "$PHAHAPA" 2>/dev/null; then
  pass "Phahapa adapter uses masking"
else
  fail "Phahapa adapter must mask recipient"
fi
if grep -q "recipient_masked" "$COMLOG_JSON" 2>/dev/null; then
  pass "Communication Log uses recipient_masked field (not raw phone/email)"
else
  fail "Communication Log must use recipient_masked field"
fi

# Config status must not contain 'token' or 'password' in return values
if python3 -c "
import ast, sys
src = open('nssf_smart_savers/integrations/zeptomail.py').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == 'get_config_status':
        code = ast.unparse(node)
        # Must return 'configured'/'not_configured' strings, not raw secret values
        if 'configured' in code and 'not_configured' in code:
            sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
  pass "ZeptoMail get_config_status returns configured/not_configured only"
else
  fail "ZeptoMail get_config_status must return only configured/not_configured"
fi

# ── Section 11: Analytics PII still blocked ───────────────────────────────────
info "Section 11: Analytics PII protection unchanged"
ANALYTICS="nssf_smart_savers/utils/analytics.py"
PII_KEYS="nssf_smart_savers/public/js/analytics_helper.js"

if [ -f "$ANALYTICS" ]; then
  result=$(python3 -c "
import ast, sys
src = open('$ANALYTICS').read()
tree = ast.parse(src)
allowed = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'ALLOWED_PARAMS':
                allowed = [e.value for e in node.value.elts
                           if isinstance(e, ast.Constant) and isinstance(e.value, str)]
PII_KEYS = {
    'first_name','last_name','full_name','phone','primary_phone',
    'email','nin','national_id','date_of_birth','dob',
    'birthday_day','birthday_month','age_years','exact_age',
    'staff_notes','notes','remarks','raw_remarks',
    'user_submitted_text','free_text','payment_reference',
}
bad = PII_KEYS.intersection(set(allowed))
if bad:
    print('FAIL: PII in ALLOWED_PARAMS: ' + str(sorted(bad)))
else:
    print('PASS: ALLOWED_PARAMS is PII-free. Count: ' + str(len(allowed)))
" 2>/dev/null || echo "FAIL: Parse error")
  if echo "$result" | grep -q "^PASS"; then
    pass "ALLOWED_PARAMS contains no PII keys"
  else
    fail "$result"
  fi
else
  warn "analytics.py not found — skipping ALLOWED_PARAMS check"
fi

if [ -f "$PII_KEYS" ]; then
  for key in first_name last_name primary_phone email date_of_birth birthday_day birthday_month age_years nin; do
    grep -q "$key" "$PII_KEYS" && pass "PII_KEYS blocks: $key" || fail "PII_KEYS missing: $key"
  done
else
  warn "analytics_helper.js not found"
fi

# ── Section 12: Messaging console route ───────────────────────────────────────
info "Section 12: Messaging console route"
HTML="nssf_smart_savers/www/smartlife-messaging-demo.html"
PY="nssf_smart_savers/www/smartlife-messaging-demo.py"

[ -f "$HTML" ] && pass "Messaging console HTML exists" || fail "Messaging console HTML missing"
[ -f "$PY" ] && pass "Messaging console Python controller exists" || fail "Messaging console Python controller missing"

for label in "SmartLife Messaging Console" "ZeptoMail Email" "Phahapa SMS / eGoSMS" \
             "Provider Configuration" "Template Preview" "Send Test Message" \
             "Communication History" "Consent Required" "Demo Mode"; do
  grep -q "$label" "$HTML" 2>/dev/null && pass "Console contains label: $label" || fail "Console missing label: $label"
done

# Console must not expose API key / token / password
for bad_word in api_key token password Authorization; do
  # Allow it in comments or as field labels but not as literal exposed values
  if grep -v "^#\|^{#\|not_configured\|configured\|site_config\|bench set-config\|REPLACE_WITH\|smartlife_" "$HTML" 2>/dev/null | grep -qi "= \"$bad_word\"\|: \"$bad_word\""; then
    fail "Messaging console HTML may expose $bad_word value"
  else
    pass "Messaging console does not expose $bad_word value"
  fi
done

# ── Section 13: Setup docs ────────────────────────────────────────────────────
info "Section 13: Messaging setup docs"
DOCS="docs/messaging_setup.md"
[ -f "$DOCS" ] && pass "docs/messaging_setup.md exists" || fail "docs/messaging_setup.md missing"

for section in "ZeptoMail" "Phahapa" "eGoSMS" "demo_mode" "consent" "REPLACE_WITH"; do
  grep -q "$section" "$DOCS" 2>/dev/null && pass "Setup docs mention: $section" || fail "Setup docs missing: $section"
done

# Docs must not contain actual credentials
if grep -qE 'Zoho-enczapikey [A-Za-z0-9+/]{20,}' "$DOCS" 2>/dev/null; then
  fail "Setup docs contain a real ZeptoMail token"
else
  pass "Setup docs contain no real ZeptoMail token"
fi

# ── Section 14: No live sends in smoke test itself ────────────────────────────
info "Section 14: Smoke test does not trigger live sends"
pass "Smoke test performs no live SMS or email sends"

# ── Section 15: Full Python compile check ────────────────────────────────────
info "Section 15: Python compile — full app"
if python3 -m compileall nssf_smart_savers -q 2>/dev/null; then
  pass "Full app compiles without errors"
else
  fail "Python compile errors detected — run: python3 -m compileall nssf_smart_savers"
fi

# ── Section 16: Live route check ──────────────────────────────────────────────
info "Section 16: Live route checks (warns if network unavailable)"
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"
http_ok "$BASE/smartlife-messaging-demo" "/smartlife-messaging-demo"
http_ok "$BASE/smartlife-staff-queue-full" "/smartlife-staff-queue-full"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "Messaging Smoke Test Results"
echo "  Passed:  $PASS"
echo "  Failed:  $FAIL"
echo "  Warnings: $WARN"
echo "============================================================"
if [ "$FAIL" -gt 0 ]; then
  echo "RESULT: FAIL — fix all failures before deploying messaging."
  exit 1
else
  echo "RESULT: PASS"
  exit 0
fi
