#!/usr/bin/env bash
set -euo pipefail

# SmartLife Phase 4: Communications & Personalisation — Smoke Test
# Run from repo root: ./scripts/smoke_test_phase_4.sh

PASS=0; FAIL=0; TOTAL=0
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"

check() {
  TOTAL=$((TOTAL + 1))
  local label="$1"; shift
  if "$@" > /dev/null 2>&1; then
    PASS=$((PASS + 1))
    printf '  ✅  %s\n' "$label"
  else
    FAIL=$((FAIL + 1))
    printf '  ❌  %s\n' "$label"
  fi
}

check_not() {
  TOTAL=$((TOTAL + 1))
  local label="$1"; shift
  if ! "$@" > /dev/null 2>&1; then
    PASS=$((PASS + 1))
    printf '  ✅  %s\n' "$label"
  else
    FAIL=$((FAIL + 1))
    printf '  ❌  %s\n' "$label"
  fi
}

echo ''
echo '══════════════════════════════════════════════════════════════'
echo '  SmartLife Phase 4 Smoke Test — Communications'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Prior smoke test syntax ──'
check 'Phase 1 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test.sh"
check 'Phase 2 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_2.sh"
check 'Phase 3 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_3.sh"
check 'Phase 4 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_4.sh"

echo ''
echo '── Communication Log DocType ──'
DOCTYPE_DIR="$APP_DIR/nssf_smart_savers/nssf_smart_savers/doctype/smartlife_communication_log"
check 'DocType directory exists' test -d "$DOCTYPE_DIR"
check 'DocType JSON exists' test -f "$DOCTYPE_DIR/smartlife_communication_log.json"
check 'DocType Python exists' test -f "$DOCTYPE_DIR/smartlife_communication_log.py"
check 'DocType __init__.py exists' test -f "$DOCTYPE_DIR/__init__.py"
check 'DocType JSON is valid JSON' python3 -c "import json; json.load(open('$DOCTYPE_DIR/smartlife_communication_log.json'))"

echo ''
echo '── Required DocType fields ──'
DT_JSON="$DOCTYPE_DIR/smartlife_communication_log.json"
for field in lead channel template_name recipient_masked message_status consent_snapshot demo_mode; do
  check "Field: $field" grep -q "\"$field\"" "$DT_JSON"
done

echo ''
echo '── Message templates ──'
TEMPLATES="$APP_DIR/nssf_smart_savers/communication_templates.py"
check 'communication_templates.py exists' test -f "$TEMPLATES"
check 'welcome_after_personal_details template defined' grep -q 'welcome_after_personal_details' "$TEMPLATES"
check 'checkout_abandoned_reminder template defined' grep -q 'checkout_abandoned_reminder' "$TEMPLATES"

echo ''
echo '── Messaging APIs in api.py ──'
API_FILE="$APP_DIR/nssf_smart_savers/api.py"
for fn in get_message_templates preview_smartlife_message send_smartlife_demo_message get_communication_history get_messaging_config_status; do
  check "API defined: $fn" grep -q "def $fn" "$API_FILE"
done

echo ''
echo '── API access control ──'
# Guest-allowed APIs
check 'get_message_templates is allow_guest=True' python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == 'get_message_templates':
    for dec in node.decorator_list:
      if isinstance(dec, ast.Call):
        for kw in dec.keywords:
          if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value == True:
            sys.exit(0)
sys.exit(1)
"

# Non-guest APIs
for fn in preview_smartlife_message send_smartlife_demo_message get_communication_history get_messaging_config_status; do
  check "$fn is NOT allow_guest" python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == '$fn':
    for dec in node.decorator_list:
      if isinstance(dec, ast.Call):
        for kw in dec.keywords:
          if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value == True:
            sys.exit(1)
    sys.exit(0)
sys.exit(1)
"
done

echo ''
echo '── Consent enforcement check ──'
MESSAGING_FILE="$APP_DIR/nssf_smart_savers/messaging.py"
check 'Consent check occurs on send' grep -q 'consent_to_contact' "$MESSAGING_FILE"

echo ''
echo '── PII protection in Log fields ──'
check 'recipient_masked field exists in JSON' grep -q '"fieldname": "recipient_masked"' "$DT_JSON"
check_not 'No raw recipient field in JSON' grep -q '"fieldname": "recipient"' "$DT_JSON"
check_not 'No phone field in JSON list' grep -q '"fieldname": "phone"' "$DT_JSON"

echo ''
echo '── Adapter credentials checks ──'
check_not 'No ZeptoMail key in integrations' grep -rn 'zeptomail_api_key.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/integrations/"
check_not 'No Phahapa key in integrations' grep -rn 'phahapa_api_key.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/integrations/"

echo ''
echo '── Python compilation ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '── Routes check ──'
HOOKS="$APP_DIR/nssf_smart_savers/hooks.py"
check 'smartlife-messaging-demo route registered' grep -q 'smartlife-messaging-demo' "$HOOKS"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Phase 4 smoke test: ALL $PASS PASSED"
else
  echo "  Phase 4 smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
