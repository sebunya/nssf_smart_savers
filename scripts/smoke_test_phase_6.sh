#!/usr/bin/env bash
set -euo pipefail

# SmartLife Phase 6: Support & Helpdesk — Smoke Test
# Run from repo root: ./scripts/smoke_test_phase_6.sh

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
echo '  SmartLife Phase 6 Smoke Test — Support & Helpdesk'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Prior smoke test syntax ──'
check 'Phase 1 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test.sh"
check 'Phase 2 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_2.sh"
check 'Phase 3 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_3.sh"
check 'Phase 4 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_4.sh"
check 'Phase 5 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_5.sh"
check 'Phase 6 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_6.sh"

echo ''
echo '── Support Request DocType ──'
DOCTYPE_DIR="$APP_DIR/nssf_smart_savers/nssf_smart_savers/doctype/smartlife_support_request"
check 'DocType directory exists' test -d "$DOCTYPE_DIR"
check 'DocType JSON exists' test -f "$DOCTYPE_DIR/smartlife_support_request.json"
check 'DocType Python exists' test -f "$DOCTYPE_DIR/smartlife_support_request.py"
check 'DocType __init__.py exists' test -f "$DOCTYPE_DIR/__init__.py"
check 'DocType JSON is valid JSON' python3 -c "import json; json.load(open('$DOCTYPE_DIR/smartlife_support_request.json'))"

echo ''
echo '── Required DocType fields ──'
DT_JSON="$DOCTYPE_DIR/smartlife_support_request.json"
for field in lead session_id support_category status consent_snapshot demo_mode; do
  check "Field: $field" grep -q "\"$field\"" "$DT_JSON"
done

echo ''
echo '── Support APIs in api.py ──'
API_FILE="$APP_DIR/nssf_smart_savers/api.py"
for fn in create_support_request get_support_requests assign_support_request update_support_status; do
  check "API defined: $fn" grep -q "def $fn" "$API_FILE"
done

echo ''
echo '── API access control ──'
# Guest-allowed APIs
check 'create_support_request is allow_guest=True' python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == 'create_support_request':
    for dec in node.decorator_list:
      if isinstance(dec, ast.Call):
        for kw in dec.keywords:
          if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value == True:
            sys.exit(0)
sys.exit(1)
"

# Non-guest APIs
for fn in get_support_requests assign_support_request update_support_status; do
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
echo '── PII and sanitisation checks ──'
check 'create_support_request uses sanitise_demo_text' grep -q 'sanitise_demo_text' "$API_FILE"
check 'create_support_request checks PII' grep -q '_check_pii' "$API_FILE"

check 'get_support_requests does NOT return message' python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == 'get_support_requests':
    code = ast.unparse(node)
    if '\"message\"' in code or '\'message\'' in code or 'resolution_notes' in code:
      sys.exit(1)
sys.exit(0)
"

echo ''
echo '── Support page content ──'
SUPPORT_HTML="$APP_DIR/nssf_smart_savers/www/smartlife-support-demo.html"
check 'Support page exists' test -f "$SUPPORT_HTML"
check 'Category options present' grep -q 'I need help joining SmartLife Flexi' "$SUPPORT_HTML"
check 'Preferred contact channel present' grep -q 'Preferred Contact Channel' "$SUPPORT_HTML"
check 'API submit integration present' grep -q 'create_support_request' "$SUPPORT_HTML"

echo ''
echo '── Python compilation ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Phase 6 smoke test: ALL $PASS PASSED"
else
  echo "  Phase 6 smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
