#!/usr/bin/env bash
set -euo pipefail

# SmartLife Demo Seed and NSSF Brand Purity — Smoke Test
# Run from repo root: ./scripts/smoke_test_demo_seed_brand.sh

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
echo '  SmartLife Demo Seed & Brand Purity Smoke Test'
echo '══════════════════════════════════════════════════════════════'
echo ''

# 1. Document Existence Checks
echo '── Document Existence Checks ──'
check 'Demo seed plan exists' test -f "$APP_DIR/docs/smartlife_demo_seed_data_plan.md"
check 'Brand cleanup review exists' test -f "$APP_DIR/docs/brand_language_cleanup_review.md"

# 2. Demo Seed Module Verification
echo ''
echo '── Demo Seed Module Verification ──'
SEED_PY="$APP_DIR/nssf_smart_savers/demo_data/smartlife_demo_seed.py"
check 'demo_data/__init__.py exists' test -f "$APP_DIR/nssf_smart_savers/demo_data/__init__.py"
check 'smartlife_demo_seed.py exists' test -f "$SEED_PY"
check 'smartlife_demo_seed.py compiles' python3 -c "import py_compile; py_compile.compile('$SEED_PY', doraise=True)"
check 'seed_demo_data defined' grep -q 'def seed_demo_data' "$SEED_PY"
check 'clear_demo_data defined' grep -q 'def clear_demo_data' "$SEED_PY"
check 'get_demo_seed_preview defined' grep -q 'def get_demo_seed_preview' "$SEED_PY"

# 3. Production Safety Verification
echo ''
echo '── Production Safety Verification ──'
HOOKS_PY="$APP_DIR/nssf_smart_savers/hooks.py"
check_not 'No auto-run in hooks.py' grep -rn 'seed_demo_data' "$HOOKS_PY"
check_not 'No real-looking NIN in seed module' grep -rn 'looks_like_nin' "$SEED_PY"
check_not 'No credential patterns in seed module' grep -rn 'sk_live\|pk_live\|SECRET_KEY' "$SEED_PY"

# 4. Fictional Persona Wording Verification
echo ''
echo '── Fictional Persona Wording Verification ──'
for id in DEMO-SMARTLIFE-001 DEMO-SMARTLIFE-002 DEMO-SMARTLIFE-003 DEMO-SMARTLIFE-004 DEMO-SMARTLIFE-005 DEMO-SMARTLIFE-006 DEMO-SMARTLIFE-007 DEMO-SMARTLIFE-008 DEMO-SMARTLIFE-009 DEMO-SMARTLIFE-010; do
  check "Scenario $id is defined in seed module" grep -q "$id" "$SEED_PY"
done

# 5. Brand Purity Verification
echo ''
echo '── Brand Purity Verification ──'
check_not 'No frappie wording anywhere' grep -rn -i 'frappie' "$APP_DIR/nssf_smart_savers/"
check_not 'No default Frappe account login message on staff queue' grep -rn 'Please sign in to your Frappe account' "$APP_DIR/nssf_smart_savers/www/"
check_not 'No default Frappe account login message in docs' grep -rn 'Please sign in to your Frappe account' "$APP_DIR/docs/"
check_not 'No NSSF blue/yellow color combination in public www templates' grep -rn -i 'blue/yellow' "$APP_DIR/nssf_smart_savers/www/"
check_not 'No dummy customer wording in public www templates' grep -rn -i 'dummy customer' "$APP_DIR/nssf_smart_savers/www/"
check_not 'No fake customer wording in public www templates' grep -rn -i 'fake customer' "$APP_DIR/nssf_smart_savers/www/"

# 6. Status and Blueprint Verification
echo ''
echo '── Status and Blueprint Verification ──'
check 'Reporting blueprint status matches' grep -q 'Reporting enhancement blueprint complete / implementation pending' "$APP_DIR/docs/smartlife_demo_seed_data_plan.md"
check 'Phase 8 status matches' grep -q 'Phase 8 release pack verified / server validation pending' "$APP_DIR/docs/smartlife_demo_seed_data_plan.md"
check 'UI/UX status matches' grep -q 'UI/UX executive professionalisation complete / server browser validation pending' "$APP_DIR/docs/smartlife_demo_seed_data_plan.md"

# 7. Python Compilation Checks
echo ''
echo '── Python Compilation Checks ──'
check 'Full Python compileall' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  Demo Seed & Brand Purity smoke test: ALL $PASS PASSED"
else
  echo "  Demo Seed & Brand Purity smoke test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
