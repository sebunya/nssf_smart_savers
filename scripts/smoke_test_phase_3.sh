#!/usr/bin/env bash
set -euo pipefail

# SmartLife Phase 3: Payment & Contribution Readiness — Smoke Test
# Run from repo root: ./scripts/smoke_test_phase_3.sh

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
echo '  SmartLife Phase 3 Smoke Test — Payment & Contribution'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Prior smoke test syntax ──'
check 'Phase 1 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test.sh"
check 'Phase 2 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_2.sh"
check 'Messaging smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_messaging.sh"
check 'Phase 3 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_3.sh"

echo ''
echo '── Contribution Intent DocType ──'
DOCTYPE_DIR="$APP_DIR/nssf_smart_savers/nssf_smart_savers/doctype/smartlife_contribution_intent"
check 'DocType directory exists' test -d "$DOCTYPE_DIR"
check 'DocType JSON exists' test -f "$DOCTYPE_DIR/smartlife_contribution_intent.json"
check 'DocType Python exists' test -f "$DOCTYPE_DIR/smartlife_contribution_intent.py"
check 'DocType __init__.py exists' test -f "$DOCTYPE_DIR/__init__.py"
check 'DocType JSON is valid JSON' python3 -c "import json; json.load(open('$DOCTYPE_DIR/smartlife_contribution_intent.json'))"

echo ''
echo '── Required DocType fields ──'
DT_JSON="$DOCTYPE_DIR/smartlife_contribution_intent.json"
for field in lead session_id saver_type contribution_amount contribution_frequency payment_method payment_status payment_reference checkout_started_on payment_completed_on pesapal_tracking_id pesapal_merchant_reference callback_status ipn_status reconciliation_status created_by_channel demo_mode failure_reason; do
  check "Field: $field" grep -q "\"$field\"" "$DT_JSON"
done

echo ''
echo '── Payment status lifecycle ──'
for status in Draft 'Checkout Started' Pending Completed Failed Cancelled Reconciled; do
  check "Status option: $status" grep -q "$status" "$DT_JSON"
done

echo ''
echo '── Payment APIs in api.py ──'
API_FILE="$APP_DIR/nssf_smart_savers/api.py"
for fn in create_payment_intent initiate_pesapal_checkout handle_pesapal_callback handle_pesapal_ipn verify_payment_status get_contribution_intent; do
  check "API defined: $fn" grep -q "def $fn" "$API_FILE"
done

echo ''
echo '── API access control ──'
# Guest-allowed APIs
for fn in create_payment_intent initiate_pesapal_checkout handle_pesapal_callback handle_pesapal_ipn; do
  check "$fn is allow_guest=True" python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == '$fn':
    for dec in node.decorator_list:
      if isinstance(dec, ast.Call):
        for kw in dec.keywords:
          if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value == True:
            sys.exit(0)
sys.exit(1)
"
done

# Non-guest APIs
for fn in verify_payment_status get_contribution_intent; do
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
echo '── Pesapal adapter ──'
PESAPAL="$APP_DIR/nssf_smart_savers/integrations/pesapal_adapter.py"
check 'pesapal_adapter.py exists' test -f "$PESAPAL"
check 'pesapal_adapter.py compiles' python3 -c "import py_compile; py_compile.compile('$PESAPAL', doraise=True)"
check 'get_auth_token defined' grep -q 'def get_auth_token' "$PESAPAL"
check 'submit_order defined' grep -q 'def submit_order' "$PESAPAL"
check 'get_transaction_status defined' grep -q 'def get_transaction_status' "$PESAPAL"
check 'Demo mode fallback present' grep -q 'is_demo_mode\|demo_mode\|DEMO_MODE' "$PESAPAL"
check 'Credentials from frappe.conf' grep -q 'frappe.conf.get' "$PESAPAL"

echo ''
echo '── Credential safety ──'
check_not 'No hardcoded Pesapal consumer key' grep -rn 'consumer_key.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/"
check_not 'No hardcoded Pesapal consumer secret' grep -rn 'consumer_secret.*=.*["'\''][A-Za-z0-9]\{10,\}' "$APP_DIR/nssf_smart_savers/"
check_not 'No Pesapal token in source' grep -rn 'pesapal.*token.*=.*["'\''][A-Za-z0-9]\{20,\}' "$APP_DIR/nssf_smart_savers/"

echo ''
echo '── PII protection ──'
check_not 'payment_reference NOT in ALLOWED_PARAMS' grep -n 'payment_reference' "$APP_DIR/nssf_smart_savers/utils/analytics.py" 2>/dev/null
check 'IPN handler returns safely' grep -q 'handle_pesapal_ipn' "$API_FILE"

echo ''
echo '── Python compilation ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '── Checkout page content ──'
CHECKOUT_HTML="$APP_DIR/nssf_smart_savers/www/smartlife-checkout-demo.html"
check 'Checkout page exists' test -f "$CHECKOUT_HTML"
check 'Plan summary present' grep -q 'Plan Summary\|plan-summary\|sl-checkout-summary' "$CHECKOUT_HTML"
check 'Payment method selector present' grep -q 'payment_method\|payment-method' "$CHECKOUT_HTML"
check 'Demo/prototype notice' grep -q 'Demo\|Prototype\|DEMO' "$CHECKOUT_HTML"
check 'Payment status display' grep -q 'payment-status\|payment_status\|sl-payment-status' "$CHECKOUT_HTML"
check 'Simulate payment preserved' grep -q 'simulate_payment\|simulatePayment\|SLCheckout' "$CHECKOUT_HTML"

echo ''
echo '── Hooks route registrations ──'
HOOKS="$APP_DIR/nssf_smart_savers/hooks.py"
check 'smartlife-staff-queue route registered' grep -q 'smartlife-staff-queue' "$HOOKS"
check 'smartlife-staff-queue-full route registered' grep -q 'smartlife-staff-queue-full' "$HOOKS"
check 'smartlife-messaging-demo route registered' grep -q 'smartlife-messaging-demo' "$HOOKS"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Phase 3 smoke test: ALL $PASS PASSED"
else
  echo "  Phase 3 smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
