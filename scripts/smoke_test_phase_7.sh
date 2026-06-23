#!/usr/bin/env bash
set -euo pipefail

# SmartLife Phase 7: Security, Privacy & Production Hardening — Smoke Test
# Run from repo root: ./scripts/smoke_test_phase_7.sh

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
echo '  SmartLife Phase 7 Smoke Test — Security & Hardening'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Prior smoke test syntax ──'
check 'Phase 1 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test.sh"
check 'Phase 2 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_2.sh"
check 'Phase 3 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_3.sh"
check 'Phase 4 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_4.sh"
check 'Phase 5 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_5.sh"
check 'Phase 6 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_6.sh"
check 'Phase 7 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_7.sh"

echo ''
echo '── Security & Privacy review document ──'
check 'Review document exists' test -f "$APP_DIR/docs/security_privacy_review.md"
check 'Review doc contains PII Inventory' grep -q 'PII Inventory' "$APP_DIR/docs/security_privacy_review.md"
check 'Review doc contains Guest Endpoint Audit' grep -q 'Guest-Open Endpoints' "$APP_DIR/docs/security_privacy_review.md"
check 'Review doc contains Role Setup guide' grep -q 'Manual Role Setup' "$APP_DIR/docs/security_privacy_review.md"

echo ''
echo '── Credential scan ──'
API_FILE="$APP_DIR/nssf_smart_savers/api.py"
check_not 'No Pesapal key in source' grep -rn 'consumer_key.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/"
check_not 'No Pesapal secret in source' grep -rn 'consumer_secret.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/"
check_not 'No ZeptoMail token in source' grep -rn 'zeptomail_api_key.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/"
check_not 'No Phahapa key in source' grep -rn 'phahapa_api_key.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/"

echo ''
echo '── Guest-Open restrictions ──'
# Verify staff-only endpoints are NOT allow_guest
for fn in get_staff_queue_full get_lead_full_detail get_communication_history get_command_centre_summary get_support_requests; do
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
echo '── Analytics PII blocks ──'
ANALYTICS_FILE="$APP_DIR/nssf_smart_savers/utils/analytics.py"
check 'ALLOWED_PARAMS defined' grep -q 'ALLOWED_PARAMS' "$ANALYTICS_FILE"
check_not 'ALLOWED_PARAMS contains no PII' python3 -c "
import sys
sys.path.append('$APP_DIR')
from nssf_smart_savers.utils.analytics import ALLOWED_PARAMS
for p in ['first_name', 'last_name', 'phone', 'email', 'nin', 'dob', 'birthday_day']:
  if p in ALLOWED_PARAMS:
    sys.exit(1)
sys.exit(0)
"

echo ''
echo '── Python compilation ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Phase 7 smoke test: ALL $PASS PASSED"
else
  echo "  Phase 7 smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
