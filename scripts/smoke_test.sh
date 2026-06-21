#!/usr/bin/env bash
# SmartLife Flexi — Comprehensive Smoke Test
# Checks routes, asset availability, CSS/JS injection, content integrity, and source-level markers.
# Run from: /home/frappe/frappe-bench/apps/nssf_smart_savers

set -euo pipefail

BASE="${SMARTLIFE_BASE_URL:-https://nssf-smartlifeflexi.nile-gov-demo.com}"
PASS=0
FAIL=0
WARN=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[PASS]${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}[FAIL]${NC} $1"; FAIL=$((FAIL+1)); }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; WARN=$((WARN+1)); }

echo "================================================================"
echo "SmartLife Flexi Smoke Test — $(date)"
echo "Base URL: $BASE"
echo "================================================================"

# ── 1. Route HTTP 200 checks ────────────────────────────────────
echo ""
echo "--- Route availability ---"
ROUTES=(
  "/smartlife-flexi-demo"
  "/smartlife-self-serve"
  "/smartlife-staff-assist"
  "/smartlife-projection-demo"
  "/smartlife-checkout-demo"
  "/smartlife-thank-you"
  "/smartlife-support-demo"
  "/helpdesk/home"
)
for ROUTE in "${ROUTES[@]}"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$BASE$ROUTE" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    ok "HTTP 200: $ROUTE"
  else
    fail "HTTP $STATUS: $ROUTE (expected 200)"
  fi
done

# ── 2. Asset availability ────────────────────────────────────────
echo ""
echo "--- Asset availability ---"
CSS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/assets/nssf_smart_savers/css/smartlife.css" 2>/dev/null || echo "000")
if [ "$CSS_STATUS" = "200" ]; then
  ok "CSS asset returns 200: /assets/nssf_smart_savers/css/smartlife.css"
else
  fail "CSS asset returned $CSS_STATUS (expected 200) — run: bench build --app nssf_smart_savers"
fi

JS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/assets/nssf_smart_savers/js/smartlife.js" 2>/dev/null || echo "000")
if [ "$JS_STATUS" = "200" ]; then
  ok "JS asset returns 200: /assets/nssf_smart_savers/js/smartlife.js"
else
  fail "JS asset returned $JS_STATUS (expected 200)"
fi

AH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/assets/nssf_smart_savers/js/analytics_helper.js" 2>/dev/null || echo "000")
if [ "$AH_STATUS" = "200" ]; then
  ok "Analytics helper JS returns 200"
else
  fail "Analytics helper JS returned $AH_STATUS (expected 200)"
fi

# ── 3. CSS/JS injection in rendered HTML ────────────────────────
echo ""
echo "--- CSS/JS injection in rendered pages ---"
check_asset_in_page() {
  local ROUTE="$1" NEEDLE="$2" LABEL="$3"
  local HTML
  HTML=$(curl -fsS --max-time 20 "$BASE$ROUTE?v=smoketest-$(date +%s)" 2>/dev/null || echo "")
  if echo "$HTML" | grep -q "$NEEDLE"; then
    ok "$LABEL: found in $ROUTE"
  else
    fail "$LABEL: NOT found in $ROUTE — CSS/JS not injected into rendered HTML"
  fi
}
check_asset_in_page "/smartlife-self-serve"       "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-staff-assist"     "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-projection-demo"  "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-checkout-demo"    "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-thank-you"        "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-flexi-demo"       "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-self-serve"       "smartlife.js"          "smartlife.js link"
check_asset_in_page "/smartlife-staff-assist"     "analytics_helper.js"   "analytics_helper.js link"

# ── 4. Design system class presence ─────────────────────────────
echo ""
echo "--- Design system class presence ---"
check_class_in_page() {
  local ROUTE="$1" CLASS="$2"
  local HTML
  HTML=$(curl -fsS --max-time 20 "$BASE$ROUTE?v=smoketest-$(date +%s)" 2>/dev/null || echo "")
  if echo "$HTML" | grep -q "$CLASS"; then
    ok "$CLASS found in $ROUTE"
  else
    fail "$CLASS NOT found in $ROUTE — design system class missing"
  fi
}
check_class_in_page "/smartlife-self-serve"      "sl-choice-card"
check_class_in_page "/smartlife-self-serve"      "sl-stepper"
check_class_in_page "/smartlife-self-serve"      "sl-step-actions"
check_class_in_page "/smartlife-staff-assist"    "sl-form"
check_class_in_page "/smartlife-staff-assist"    "sl-select"
check_class_in_page "/smartlife-projection-demo" "sl-result-card"
check_class_in_page "/smartlife-checkout-demo"   "sl-summary"

# ── 5. Required content strings ──────────────────────────────────
echo ""
echo "--- Required content strings ---"
check_content_in_page() {
  local ROUTE="$1" STRING="$2"
  local HTML
  HTML=$(curl -fsS --max-time 20 "$BASE$ROUTE?v=smoketest-$(date +%s)" 2>/dev/null || echo "")
  if echo "$HTML" | grep -qi "$STRING"; then
    ok "\"$STRING\" found in $ROUTE"
  else
    fail "\"$STRING\" NOT found in $ROUTE"
  fi
}

# Self-serve: 5 saver types
check_content_in_page "/smartlife-self-serve" "Existing NSSF Member"
check_content_in_page "/smartlife-self-serve" "New Saver"
check_content_in_page "/smartlife-self-serve" "Diaspora Saver"
check_content_in_page "/smartlife-self-serve" "Informal Sector"
check_content_in_page "/smartlife-self-serve" "Staff-Assisted"
check_content_in_page "/smartlife-self-serve" "Who are you saving as"

# Staff assist
check_content_in_page "/smartlife-staff-assist" "Staff-Guided Session"
check_content_in_page "/smartlife-staff-assist" "Prospect Segment"
check_content_in_page "/smartlife-staff-assist" "Savings Goal"

# Projection
check_content_in_page "/smartlife-projection-demo" "Savings Projection Calculator"
check_content_in_page "/smartlife-projection-demo" "Projection is indicative"
check_content_in_page "/smartlife-projection-demo" "Semi-Annually"

# Demo safety
check_content_in_page "/smartlife-self-serve"      "Prototype environment"
check_content_in_page "/smartlife-staff-assist"    "Prototype environment"
check_content_in_page "/smartlife-projection-demo" "Prototype environment"
check_content_in_page "/smartlife-checkout-demo"   "Prototype environment"

# Checkout / thank-you
check_content_in_page "/smartlife-checkout-demo" "SmartLife Flexi"
check_content_in_page "/smartlife-thank-you"     "Thank"

# ── 6. Analytics / GTM checks (warn, not fail) ──────────────────
echo ""
echo "--- Analytics / GTM (warnings only) ---"
GTM_HTML=$(curl -fsS --max-time 20 "$BASE/smartlife-flexi-demo?v=smoketest-$(date +%s)" 2>/dev/null || echo "")
if echo "$GTM_HTML" | grep -q "GTM-PZRV3MQL\|analytics_helper"; then
  ok "GTM or analytics_helper found in landing page"
else
  warn "GTM-PZRV3MQL not found in smartlife-flexi-demo — check hooks.py web_include_js or template includes"
fi
if echo "$GTM_HTML" | grep -qi "uvlttflnbt\|clarity"; then
  ok "Microsoft Clarity ID found in landing page"
else
  warn "Clarity ID uvlttflnbt not detected in landing page — check GTM configuration"
fi

# ── 7. Source-level checks ───────────────────────────────────────
echo ""
echo "--- Source-level checks ---"
if [ -f "nssf_smart_savers/www/smartlife-self-serve.html" ]; then
  grep -q "smartlife.css" nssf_smart_savers/www/smartlife-self-serve.html \
    && ok "Source: smartlife.css link in self-serve.html" \
    || fail "Source: smartlife.css link MISSING from self-serve.html"

  grep -q "sl-choice-card" nssf_smart_savers/www/smartlife-self-serve.html \
    && ok "Source: sl-choice-card in self-serve.html" \
    || fail "Source: sl-choice-card MISSING from self-serve.html"

  grep -q "Existing NSSF Member" nssf_smart_savers/www/smartlife-self-serve.html \
    && ok "Source: 'Existing NSSF Member' hardcoded in self-serve.html" \
    || fail "Source: 'Existing NSSF Member' NOT in self-serve.html"
fi

if [ -f "nssf_smart_savers/www/smartlife-staff-assist.html" ]; then
  grep -q "sl-form" nssf_smart_savers/www/smartlife-staff-assist.html \
    && ok "Source: sl-form in staff-assist.html" \
    || fail "Source: sl-form MISSING from staff-assist.html"

  grep -q "sl-select" nssf_smart_savers/www/smartlife-staff-assist.html \
    && ok "Source: sl-select in staff-assist.html" \
    || fail "Source: sl-select MISSING from staff-assist.html"
fi

if [ -f "nssf_smart_savers/www/smartlife-projection-demo.html" ]; then
  grep -q "sl-result-card" nssf_smart_savers/www/smartlife-projection-demo.html \
    && ok "Source: sl-result-card in projection-demo.html" \
    || fail "Source: sl-result-card MISSING from projection-demo.html"

  grep -qi "semi-annually" nssf_smart_savers/www/smartlife-projection-demo.html \
    && ok "Source: semi-annually frequency in projection-demo.html" \
    || fail "Source: semi-annually MISSING from projection-demo.html"
fi

# Check no PII test values in source
for f in nssf_smart_savers/www/smartlife-*.html; do
  if grep -qiE "CM\d{7}[A-Z]{2}|\+2567[0-9]{8}|@gmail\.com|@yahoo\.com" "$f" 2>/dev/null; then
    fail "Source: Possible PII test value detected in $f"
  else
    ok "Source: No PII test values in $(basename $f)"
  fi
done

# CSS has all required design classes
if [ -f "nssf_smart_savers/public/css/smartlife.css" ]; then
  for CLASS in ".sl-page" ".sl-container" ".sl-card" ".sl-choice-card" ".sl-goal-card" ".sl-stepper" ".sl-btn-primary" ".sl-result-card" ".sl-table" ".sl-form" ".sl-input" ".sl-select"; do
    grep -q "$CLASS" nssf_smart_savers/public/css/smartlife.css \
      && ok "CSS: $CLASS defined" \
      || fail "CSS: $CLASS MISSING — design system incomplete"
  done
fi

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "================================================================"
echo -e "Results: ${GREEN}$PASS passed${NC} | ${RED}$FAIL failed${NC} | ${YELLOW}$WARN warnings${NC}"
echo "================================================================"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo -e "${RED}SMOKE TEST FAILED${NC} — $FAIL check(s) did not pass."
  echo "Common causes:"
  echo "  1. Run: bench build --app nssf_smart_savers"
  echo "  2. Run: bench --site \$SITE clear-cache && clear-website-cache"
  echo "  3. Check that web_include_css/js in hooks.py are correct"
  echo "  4. Verify templates contain explicit <link rel=\"stylesheet\"> tags"
  echo "  5. Check Cloudflare cache — purge if needed"
  exit 1
else
  echo -e "${GREEN}SMOKE TEST PASSED${NC}"
  exit 0
fi
