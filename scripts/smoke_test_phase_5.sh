#!/usr/bin/env bash
set -euo pipefail

# SmartLife Phase 5: Command Centre and Analytics — Smoke Test
# Run from repo root: ./scripts/smoke_test_phase_5.sh

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
echo '  SmartLife Phase 5 Smoke Test — Command Centre'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Prior smoke test syntax ──'
check 'Phase 1 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test.sh"
check 'Phase 2 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_2.sh"
check 'Phase 3 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_3.sh"
check 'Phase 4 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_4.sh"
check 'Phase 5 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_5.sh"

echo ''
echo '── Command Centre dashboard files ──'
check 'Dashboard HTML exists' test -f "$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.html"
check 'Dashboard Controller exists' test -f "$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.py"
check 'Dashboard HTML extends web.html' grep -q "{% extends \"templates/web.html\" %}" "$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.html"
check 'Dashboard HTML includes brand shell' grep -q "smartlife_brand_shell.html" "$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.html"
check 'Dashboard HTML includes guest gate' grep -q "is_guest" "$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.html"

echo ''
echo '── Dashboard controller validation ──'
PY_FILE="$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.py"
check 'is_demo is set to True' grep -q "context.is_demo = True" "$PY_FILE"
check 'no_breadcrumbs is set to True' grep -q "context.no_breadcrumbs = True" "$PY_FILE"
check 'has_personalisation_role check is present' grep -q "has_personalisation_role" "$PY_FILE"
check 'Guest check is present' grep -q "is_guest = frappe.session.user == \"Guest\"" "$PY_FILE"

echo ''
echo '── Command Centre APIs in api.py ──'
API_FILE="$APP_DIR/nssf_smart_savers/api.py"
for fn in get_command_centre_summary get_conversion_funnel get_dropoff_by_stage get_lead_distribution get_campaign_performance get_birth_month_distribution; do
  check "API defined: $fn" grep -q "def $fn" "$API_FILE"
done

echo ''
echo '── API access control (No allow_guest=True) ──'
for fn in get_command_centre_summary get_conversion_funnel get_dropoff_by_stage get_lead_distribution get_campaign_performance get_birth_month_distribution; do
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
echo '── PII safety in Command Centre APIs ──'
check 'get_birth_month_distribution does NOT return birthday_day' python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == 'get_birth_month_distribution':
    code = ast.unparse(node)
    if 'birthday_day' in code or 'primary_phone' in code:
      sys.exit(1)
sys.exit(0)
"

check 'get_lead_distribution has strict allowlist of fields' python3 -c "
import ast, sys
tree = ast.parse(open('$API_FILE').read())
for node in ast.walk(tree):
  if isinstance(node, ast.FunctionDef) and node.name == 'get_lead_distribution':
    code = ast.unparse(node)
    if 'first_name' in code or 'email' in code or 'phone' in code:
      sys.exit(1)
sys.exit(0)
"

echo ''
echo '── Hooks route registration ──'
HOOKS="$APP_DIR/nssf_smart_savers/hooks.py"
check 'smartlife-command-centre route registered' grep -q 'smartlife-command-centre' "$HOOKS"

echo ''
echo '── Python compilation ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Phase 5 smoke test: ALL $PASS PASSED"
else
  echo "  Phase 5 smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
