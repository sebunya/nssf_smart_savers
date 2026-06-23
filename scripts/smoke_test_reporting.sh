#!/usr/bin/env bash
set -euo pipefail

# SmartLife Reporting & Analytics Blueprint — Smoke Test
# Run from repo root: ./scripts/smoke_test_reporting.sh

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
echo '  SmartLife Reporting & Analytics Blueprint Smoke Test'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Document Existence Checks ──'
check 'Strategy document exists' test -f "$APP_DIR/docs/smartlife_reporting_charts_strategy.md"
check 'Metric dictionary exists' test -f "$APP_DIR/docs/smartlife_reporting_metric_dictionary.md"
check 'Board reporting pack exists' test -f "$APP_DIR/docs/smartlife_board_reporting_pack.md"
check 'Personalisation manager pack exists' test -f "$APP_DIR/docs/smartlife_personalisation_manager_reporting_pack.md"
check 'Implementation plan exists' test -f "$APP_DIR/docs/smartlife_reporting_implementation_plan.md"
check 'Reporting execution notes exist' test -f "$APP_DIR/docs/reporting_local_execution_notes.md"

echo ''
echo '── Command Centre Access & Security Guards ──'
COMMAND_CENTRE_PY="$APP_DIR/nssf_smart_savers/www/smartlife-command-centre.py"
check 'Command Centre checks for personalization role' grep -q "SmartLife Personalisation Team" "$COMMAND_CENTRE_PY"
check 'Command Centre verifies non-guest' grep -q "frappe.session.user == \"Guest\"" "$COMMAND_CENTRE_PY"

echo ''
echo '── Document Content Safety Checks ──'
check_not 'Strategy doc does not claim production ready' grep -qi 'production ready' "$APP_DIR/docs/smartlife_reporting_charts_strategy.md"
check_not 'Implementation plan does not claim production ready' grep -qi 'production ready' "$APP_DIR/docs/smartlife_reporting_implementation_plan.md"
check 'Strategy doc defines small-count suppression' grep -qi 'small-count suppression' "$APP_DIR/docs/smartlife_reporting_charts_strategy.md"
check 'Implementation plan details Option D' grep -q 'Option D' "$APP_DIR/docs/smartlife_reporting_implementation_plan.md"
check 'Reporting status is blueprint complete' grep -q 'Reporting enhancement blueprint complete / implementation pending' "$APP_DIR/docs/reporting_local_execution_notes.md"

echo ''
echo '── Existing UI & Code Protection Checks ──'
check 'Python files compile without error' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"
check 'UI/UX smoke test script remains intact' test -f "$APP_DIR/scripts/smoke_test_ui_ux.sh"
check 'Phase 8 smoke test script remains intact' test -f "$APP_DIR/scripts/smoke_test_phase_8.sh"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Reporting Smoke Test: ALL $PASS PASSED"
else
  echo "  Reporting Smoke Test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
