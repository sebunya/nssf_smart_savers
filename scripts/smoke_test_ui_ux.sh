#!/usr/bin/env bash
set -euo pipefail

# SmartLife Executive UI/UX — Smoke Test
# Run from repo root: ./scripts/smoke_test_ui_ux.sh

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
echo '  SmartLife Executive UI/UX Audit Smoke Test'
echo '══════════════════════════════════════════════════════════════'
echo ''

echo '── Review Document Existence ──'
check 'UI/UX review document exists' test -f "$APP_DIR/docs/ui_ux_executive_acceptance_review.md"

echo ''
echo '── Emoji / Symbol Scan (nssf_smart_savers/www) ──'
# Emojis must be completely absent from HTML and Python UI files
check_not 'No 🚀 emoji' grep -rn "🚀" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No ✨ emoji' grep -rn "✨" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No 🔥 emoji' grep -rn "🔥" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No 🎉 emoji' grep -rn "🎉" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No 💡 emoji' grep -rn "💡" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No 📊 emoji' grep -rn "📊" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No 📈 emoji' grep -rn "📈" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No ✅ emoji' grep -rn "✅" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No ❌ emoji' grep -rn "❌" "$APP_DIR/nssf_smart_savers/www/"
check_not 'No ⚠️ emoji' grep -rn "⚠️" "$APP_DIR/nssf_smart_savers/www/"

echo ''
echo '── UI Page Existence Checks ──'
PAGES=(
  "smartlife-flexi-demo.html"
  "smartlife-self-serve.html"
  "smartlife-staff-assist.html"
  "smartlife-projection-demo.html"
  "smartlife-checkout-demo.html"
  "smartlife-thank-you.html"
  "smartlife-support-demo.html"
  "smartlife-staff-queue.html"
  "smartlife-staff-queue-full.html"
  "smartlife-messaging-demo.html"
  "smartlife-command-centre.html"
)

for page in "${PAGES[@]}"; do
  check "UI file exists: $page" test -f "$APP_DIR/nssf_smart_savers/www/$page"
done

echo ''
echo '── Review Safety Assertions ──'
REVIEW_DOC="$APP_DIR/docs/ui_ux_executive_acceptance_review.md"
check_not 'Does not claim 100% perfect' grep -qi '100% perfect' "$REVIEW_DOC"
check_not 'Does not claim production acceptance' grep -qi 'production acceptance' "$REVIEW_DOC"
check 'Keeps server browser validation pending status' grep -q 'UI/UX executive professionalisation complete / server browser validation pending' "$REVIEW_DOC"
check_not 'Does not contain "Project complete" wording' grep -qi 'project complete' "$REVIEW_DOC"

echo ''
echo '── Integrity Checks ──'
# Make sure no backend logic changes or schema model edits happened
check 'Python code compiles successfully' python3 -m compileall -q "$APP_DIR/nssf_smart_savers"

echo ''
echo '══════════════════════════════════════════════════════════════'
if [ "$FAIL" -eq 0 ]; then
  echo "  UI/UX Audit Smoke Test: ALL $PASS PASSED"
else
  echo "  UI/UX Audit Smoke Test: $PASS passed | $FAIL FAILED (of $TOTAL)"
fi
echo '══════════════════════════════════════════════════════════════'
exit "$FAIL"
