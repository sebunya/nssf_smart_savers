#!/usr/bin/env bash
# SmartLife Flexi — Smoke Test
# v nssf-brand-shell-tempfile-20260622
#
# Uses temp files for page fetches so grep never sees file paths
# mixed into the HTML content (which caused false negatives).
#
# Checks:
#   1. Route HTTP 200s
#   2. Asset HTTP 200s
#   3. CSS/JS presence in rendered HTML
#   4. Brand shell presence (sl-brand-shell, sl-brand-bar, sl-demo-route)
#   5. Design system class presence
#   6. Required content strings (DOB, saver types, staff-assist, projection)
#   7. Analytics / GTM (warn-only)
#   8. Source-level markers (NSSF colours, brand shell, DOB, no manual age)
#   9. API and DocType integrity
#
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

# ── Temp dir for page files ──────────────────────────────────────
# All fetched pages are written to individual files.
# grep then operates on the file, never sees the path mixed with content.
TMPDIR_SMOKE="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_SMOKE"' EXIT

fetch_page() {
  local route="$1"
  local slug
  slug="$(echo "$route" | tr '/' '_')"
  local outfile="$TMPDIR_SMOKE/${slug}.html"
  curl -sSL --max-time 25 \
    --header "Cache-Control: no-cache, no-store" \
    --header "Pragma: no-cache" \
    "$BASE$route?v=smoketest-$(date +%s)-$RANDOM" \
    -o "$outfile" 2>/dev/null
  printf "%s" "$outfile"
}

contains_file() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Eiq "$pattern" "$file" 2>/dev/null; then
    ok "$label"
  else
    fail "$label"
    echo "       Diagnostic (first matching asset/brand lines):"
    grep -Ein "smartlife|sl-brand|sl-demo|sl-stepper|sl-choice|Date of birth|NSSF|stylesheet|\.css|\.js" \
      "$file" 2>/dev/null | head -20 || echo "       (none found)"
  fi
}

# ── 1. Route HTTP 200 checks ─────────────────────────────────────
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
)
declare -A ROUTE_FILES
for ROUTE in "${ROUTES[@]}"; do
  STATUS=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 15 "$BASE$ROUTE" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    ok "HTTP 200: $ROUTE"
    ROUTE_FILES["$ROUTE"]="$(fetch_page "$ROUTE")"
  else
    fail "HTTP $STATUS: $ROUTE (expected 200)"
    ROUTE_FILES["$ROUTE"]="/dev/null"
  fi
done

# ── 2. Asset availability ─────────────────────────────────────────
echo ""
echo "--- Asset availability ---"
_asset_check() {
  local APATH="$1" LABEL="$2"
  local STATUS
  STATUS=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$APATH" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    ok "Asset 200: $LABEL"
  else
    fail "Asset $STATUS: $LABEL — run: bench build --app nssf_smart_savers"
  fi
}
_asset_check "/assets/nssf_smart_savers/css/smartlife.css" "smartlife.css"
_asset_check "/assets/nssf_smart_savers/js/smartlife.js"   "smartlife.js"
_asset_check "/assets/nssf_smart_savers/js/analytics_helper.js" "analytics_helper.js"

# ── 3. CSS/JS in rendered HTML ────────────────────────────────────
echo ""
echo "--- CSS/JS in rendered HTML ---"
contains_file "${ROUTE_FILES[/smartlife-self-serve]}"      "smartlife\.css"        "smartlife.css in /smartlife-self-serve"
contains_file "${ROUTE_FILES[/smartlife-staff-assist]}"    "smartlife\.css"        "smartlife.css in /smartlife-staff-assist"
contains_file "${ROUTE_FILES[/smartlife-projection-demo]}" "smartlife\.css"        "smartlife.css in /smartlife-projection-demo"
contains_file "${ROUTE_FILES[/smartlife-checkout-demo]}"   "smartlife\.css"        "smartlife.css in /smartlife-checkout-demo"
contains_file "${ROUTE_FILES[/smartlife-thank-you]}"       "smartlife\.css"        "smartlife.css in /smartlife-thank-you"
contains_file "${ROUTE_FILES[/smartlife-flexi-demo]}"      "smartlife\.css"        "smartlife.css in /smartlife-flexi-demo"
contains_file "${ROUTE_FILES[/smartlife-self-serve]}"      "smartlife\.js"         "smartlife.js in /smartlife-self-serve"
contains_file "${ROUTE_FILES[/smartlife-staff-assist]}"    "analytics_helper\.js"  "analytics_helper.js in /smartlife-staff-assist"

# ── 4. Brand shell presence ───────────────────────────────────────
echo ""
echo "--- Brand shell and navbar suppression ---"
for ROUTE in "/smartlife-self-serve" "/smartlife-staff-assist" "/smartlife-projection-demo" \
             "/smartlife-checkout-demo" "/smartlife-thank-you" "/smartlife-flexi-demo"; do
  F="${ROUTE_FILES[$ROUTE]}"
  contains_file "$F" "sl-brand-shell|sl-brand-bar" "Brand shell in $ROUTE"
  contains_file "$F" "sl-demo-route"                "sl-demo-route class in $ROUTE"
  contains_file "$F" "NSSF SmartLife Flexi"         "Brand title in $ROUTE"
done

# ── 5. Design system classes ──────────────────────────────────────
echo ""
echo "--- Design system class presence ---"
contains_file "${ROUTE_FILES[/smartlife-self-serve]}"      "sl-choice-card"  "sl-choice-card in self-serve"
contains_file "${ROUTE_FILES[/smartlife-self-serve]}"      "sl-stepper"      "sl-stepper in self-serve"
contains_file "${ROUTE_FILES[/smartlife-self-serve]}"      "sl-step-actions" "sl-step-actions in self-serve"
contains_file "${ROUTE_FILES[/smartlife-self-serve]}"      "sl-form"         "sl-form in self-serve"
contains_file "${ROUTE_FILES[/smartlife-staff-assist]}"    "sl-form"         "sl-form in staff-assist"
contains_file "${ROUTE_FILES[/smartlife-staff-assist]}"    "sl-select"       "sl-select in staff-assist"
contains_file "${ROUTE_FILES[/smartlife-projection-demo]}" "sl-result-card"  "sl-result-card in projection-demo"
contains_file "${ROUTE_FILES[/smartlife-checkout-demo]}"   "sl-summary"      "sl-summary in checkout-demo"

# ── 6. Required content strings ───────────────────────────────────
echo ""
echo "--- Required content strings ---"
F_SS="${ROUTE_FILES[/smartlife-self-serve]}"
F_SA="${ROUTE_FILES[/smartlife-staff-assist]}"
F_PR="${ROUTE_FILES[/smartlife-projection-demo]}"
F_CO="${ROUTE_FILES[/smartlife-checkout-demo]}"
F_TY="${ROUTE_FILES[/smartlife-thank-you]}"

contains_file "$F_SS" "Existing NSSF Member"    "Existing NSSF Member in self-serve"
contains_file "$F_SS" "New Saver"               "New Saver in self-serve"
contains_file "$F_SS" "Diaspora Saver"          "Diaspora Saver in self-serve"
contains_file "$F_SS" "Informal Sector"         "Informal Sector in self-serve"
contains_file "$F_SS" "Staff-Assisted"          "Staff-Assisted in self-serve"
contains_file "$F_SS" "Who are you saving as"   "Step 1 heading in self-serve"
contains_file "$F_SS" "Your Personal Details"   "Step 2 heading in self-serve"
contains_file "$F_SS" "Date of birth"           "DOB field label in self-serve"
contains_file "$F_SS" "date_of_birth"           "date_of_birth name attr in self-serve"
contains_file "$F_SS" "phone"                   "Phone field in self-serve"
contains_file "$F_SS" "consent"                 "Consent field in self-serve"
contains_file "$F_SS" "Prototype environment"   "Prototype notice in self-serve"
contains_file "$F_SA" "Staff-Guided Session"    "Staff-Guided Session heading"
contains_file "$F_SA" "Prospect Segment"        "Prospect Segment in staff-assist"
contains_file "$F_SA" "Savings Goal"            "Savings Goal in staff-assist"
contains_file "$F_SA" "Prototype environment"   "Prototype notice in staff-assist"
contains_file "$F_PR" "Savings Projection"      "Savings Projection heading"
contains_file "$F_PR" "Projection is indicative" "Indicative disclaimer in projection"
contains_file "$F_PR" "Semi-Annually"           "Semi-Annually in projection"
contains_file "$F_PR" "Prototype environment"   "Prototype notice in projection"
contains_file "$F_CO" "SmartLife Flexi"         "SmartLife Flexi in checkout"
contains_file "$F_CO" "Prototype environment"   "Prototype notice in checkout"
contains_file "$F_TY" "SmartLife\|Thank\|on your way" "Thank-you landing content"

# ── 7. Analytics / GTM (warn only) ───────────────────────────────
echo ""
echo "--- Analytics / GTM (warnings only) ---"
F_LD="${ROUTE_FILES[/smartlife-flexi-demo]}"
if grep -Eq "GTM-PZRV3MQL|analytics_helper" "$F_LD" 2>/dev/null; then
  ok "GTM or analytics_helper found in landing page"
else
  warn "GTM-PZRV3MQL not found in smartlife-flexi-demo — check hooks.py"
fi
if grep -Eiq "uvlttflnbt|clarity" "$F_LD" 2>/dev/null; then
  ok "Microsoft Clarity ID found in landing page"
else
  warn "Clarity ID not detected — check GTM configuration"
fi

# ── 8. Source-level checks ────────────────────────────────────────
echo ""
echo "--- Source-level checks ---"

CSS_FILE="nssf_smart_savers/public/css/smartlife.css"
if [ -f "$CSS_FILE" ]; then
  for CLASS in ".sl-page" ".sl-container" ".sl-card" ".sl-choice-card" ".sl-goal-card" \
               ".sl-stepper" ".sl-step" ".sl-btn-primary" ".sl-btn-secondary" \
               ".sl-form" ".sl-input" ".sl-select" ".sl-result-card" \
               ".sl-table" ".sl-summary" ".sl-alert" ".sl-disclaimer" \
               ".sl-brand-shell" ".sl-brand-bar" ".sl-brand-lockup"; do
    grep -q "$CLASS" "$CSS_FILE" \
      && ok "CSS: $CLASS defined" \
      || fail "CSS: $CLASS MISSING"
  done
  for COLOUR in "#002060" "#0F2C59" "#00AEEF" "#00A3E0" "#00A859" "#107C41"; do
    grep -qi "$COLOUR" "$CSS_FILE" \
      && ok "CSS: NSSF colour $COLOUR present" \
      || fail "CSS: NSSF colour $COLOUR MISSING"
  done
else
  fail "CSS file not found: $CSS_FILE"
fi

AH_FILE="nssf_smart_savers/public/js/analytics_helper.js"
if [ -f "$AH_FILE" ]; then
  for BLOCKED_KEY in "first_name" "last_name" "phone" "email" "nin" "date_of_birth" "age_years"; do
    grep -q "$BLOCKED_KEY" "$AH_FILE" \
      && ok "Analytics: '$BLOCKED_KEY' in PII block-list" \
      || fail "Analytics: '$BLOCKED_KEY' NOT in PII block-list"
  done
  grep -q "PII_KEYS\|isPiiKey\|sanitise" "$AH_FILE" \
    && ok "Analytics: PII guard present" \
    || fail "Analytics: PII guard MISSING"
else
  fail "analytics_helper.js not found"
fi

SS_FILE="nssf_smart_savers/www/smartlife-self-serve.html"
if [ -f "$SS_FILE" ]; then
  grep -q "smartlife\.css\|smartlife.css" "$SS_FILE" \
    && ok "Source: smartlife.css link in self-serve.html" \
    || fail "Source: smartlife.css MISSING"
  grep -q "sl-choice-card" "$SS_FILE"    && ok "Source: sl-choice-card in self-serve.html"    || fail "Source: sl-choice-card MISSING"
  grep -q "Existing NSSF Member" "$SS_FILE" && ok "Source: 'Existing NSSF Member' found"     || fail "Source: 'Existing NSSF Member' NOT found"
  grep -q "date_of_birth" "$SS_FILE"     && ok "Source: date_of_birth in self-serve.html"     || fail "Source: date_of_birth MISSING"
  grep -qi "Date of birth" "$SS_FILE"    && ok "Source: 'Date of birth' label found"          || fail "Source: 'Date of birth' MISSING"
  grep -q "smartlife_brand_shell" "$SS_FILE" && ok "Source: brand shell include in self-serve" || fail "Source: brand shell include MISSING"
  if grep -q 'id="sl-age"' "$SS_FILE"; then
    fail "Source: manual age input (id=sl-age) still present — must be DOB"
  else
    ok "Source: manual age input correctly absent"
  fi
fi

SA_FILE="nssf_smart_savers/www/smartlife-staff-assist.html"
if [ -f "$SA_FILE" ]; then
  grep -q "sl-form"   "$SA_FILE" && ok "Source: sl-form in staff-assist.html"   || fail "Source: sl-form MISSING"
  grep -q "sl-select" "$SA_FILE" && ok "Source: sl-select in staff-assist.html" || fail "Source: sl-select MISSING"
  grep -q "smartlife_brand_shell" "$SA_FILE" && ok "Source: brand shell include in staff-assist" || fail "Source: brand shell include MISSING"
fi

PROJ_FILE="nssf_smart_savers/www/smartlife-projection-demo.html"
if [ -f "$PROJ_FILE" ]; then
  grep -q "sl-result-card" "$PROJ_FILE" && ok "Source: sl-result-card in projection-demo.html" || fail "Source: sl-result-card MISSING"
  grep -qi "semi-annually"  "$PROJ_FILE" && ok "Source: semi-annually in projection-demo.html"  || fail "Source: semi-annually MISSING"
fi

API_FILE="nssf_smart_savers/api.py"
if [ -f "$API_FILE" ]; then
  grep -q "date_of_birth"  "$API_FILE" && ok "API: date_of_birth accepted"  || fail "API: date_of_birth NOT found"
  grep -q "birthday_month" "$API_FILE" && ok "API: birthday_month computed" || fail "API: birthday_month NOT found"
  grep -q "birthday_day"   "$API_FILE" && ok "API: birthday_day computed"   || fail "API: birthday_day NOT found"
  grep -q "age_band"       "$API_FILE" && ok "API: age_band computed"       || fail "API: age_band NOT found"
else
  fail "api.py not found"
fi

DT_FILE="nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json"
if [ -f "$DT_FILE" ]; then
  for DT_FIELD in "date_of_birth" "birthday_month" "birthday_day" "age_years" "age_band" \
                  "primary_phone" "gender" "consent_to_contact"; do
    grep -q "\"$DT_FIELD\"" "$DT_FILE" \
      && ok "DocType: $DT_FIELD present" \
      || fail "DocType: $DT_FIELD MISSING"
  done
else
  fail "DocType JSON not found: $DT_FILE"
fi

for f in nssf_smart_savers/www/smartlife-*.html; do
  if grep -qiE "CM[0-9]{7}[A-Z]{2}|\+2567[0-9]{8}|@gmail\.com|@yahoo\.com" "$f" 2>/dev/null; then
    fail "Source: PII test value in $(basename "$f")"
  else
    ok "Source: no PII test values in $(basename "$f")"
  fi
done

for f in nssf_smart_savers/www/smartlife-*.html; do
  grep -q "Cache-Control" "$f" \
    && ok "Source: no-cache header in $(basename "$f")" \
    || warn "Source: no-cache header MISSING from $(basename "$f")"
done

# ── Summary ───────────────────────────────────────────────────────
echo ""
echo "================================================================"
echo -e "Results: ${GREEN}$PASS passed${NC} | ${RED}$FAIL failed${NC} | ${YELLOW}$WARN warnings${NC}"
echo "================================================================"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo -e "${RED}SMOKE TEST FAILED${NC} — $FAIL check(s) did not pass."
  echo ""
  echo "Common causes:"
  echo "  1. bench build --app nssf_smart_savers"
  echo "  2. bench --site \$SITE clear-cache && bench --site \$SITE clear-website-cache"
  echo "  3. If brand shell checks fail: template include may not be rendering"
  echo "  4. If origin passes but public fails: purge Cloudflare cache"
  exit 1
else
  echo -e "${GREEN}ALL CHECKS PASSED${NC}"
  exit 0
fi
