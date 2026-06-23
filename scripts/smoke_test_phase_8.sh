#!/usr/bin/env bash
set -euo pipefail

# SmartLife Phase 8: Release Pack and Production Readiness — Smoke Test
# Run from repo root: ./scripts/smoke_test_phase_8.sh

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
echo '  SmartLife Phase 8 Smoke Test — Release Pack'
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
check 'Phase 8 smoke test syntax valid' bash -n "$APP_DIR/scripts/smoke_test_phase_8.sh"

echo ''
echo '── Document Existence Checks ──'
DOCS=(
  "phase_8_release_pack.md"
  "server_operator_validation_runbook.md"
  "release_acceptance_checklist.md"
  "release_rollback_plan.md"
  "environment_configuration_checklist.md"
  "final_technical_inventory.md"
  "phase_2_to_8_release_notes.md"
  "nssf_smartlife_demo_walkthrough.md"
  "admin_user_guide.md"
  "staff_user_guide.md"
  "demo_script.md"
  "known_limitations.md"
  "production_readiness_checklist.md"
)

for doc in "${DOCS[@]}"; do
  check "Document exists: $doc" test -f "$APP_DIR/docs/$doc"
done

echo ''
echo '── Document Content Verification ──'
check 'production_readiness_checklist.md has DPO sign-off' grep -qi 'dpo sign-off' "$APP_DIR/docs/production_readiness_checklist.md"
check 'demo_script.md has landing step' grep -qi 'landing' "$APP_DIR/docs/demo_script.md"
check 'demo_script.md has projection step' grep -qi 'projection' "$APP_DIR/docs/demo_script.md"
check 'demo_script.md has checkout step' grep -qi 'checkout' "$APP_DIR/docs/demo_script.md"
check 'demo_script.md has command centre step' grep -qi 'command centre' "$APP_DIR/docs/demo_script.md"
check 'known_limitations.md mentions rate limiting' grep -qi 'rate limit' "$APP_DIR/docs/known_limitations.md"
check 'known_limitations.md mentions demo environment' grep -qi 'demo environment' "$APP_DIR/docs/known_limitations.md"

echo ''
echo '── Python compilation ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Phase 8 smoke test: ALL $PASS PASSED"
else
  echo "  Phase 8 smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
