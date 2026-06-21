#!/usr/bin/env bash
set -euo pipefail

SITE_NAME="${SITE_NAME:-nssf-smartlifeflexi.nile-gov-demo.com}"
BENCH_PATH="${BENCH_PATH:-/home/frappe/frappe-bench}"
APP_NAME="${APP_NAME:-nssf_smart_savers}"

echo "Running SmartLife Flexi smoke tests for $SITE_NAME"

cd "$BENCH_PATH"

echo "1. Checking installed apps..."
bench --site "$SITE_NAME" list-apps | grep -q "$APP_NAME"
echo "OK: $APP_NAME is installed"

echo "2. Checking homepage..."
curl -fsSI "https://$SITE_NAME" >/dev/null
echo "OK: Homepage responds"

echo "3. Checking /smartlife-flexi-demo -> 200..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "https://$SITE_NAME/smartlife-flexi-demo")
[ "$HTTP_CODE" = "200" ] && echo "OK: /smartlife-flexi-demo -> 200" || { echo "FAIL: /smartlife-flexi-demo -> $HTTP_CODE"; exit 1; }

echo "4. Checking /smartlife-self-serve -> 200..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "https://$SITE_NAME/smartlife-self-serve")
[ "$HTTP_CODE" = "200" ] && echo "OK: /smartlife-self-serve -> 200" || { echo "FAIL: /smartlife-self-serve -> $HTTP_CODE"; exit 1; }

echo "5. Checking /smartlife-staff-assist -> 200..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "https://$SITE_NAME/smartlife-staff-assist")
[ "$HTTP_CODE" = "200" ] && echo "OK: /smartlife-staff-assist -> 200" || { echo "FAIL: /smartlife-staff-assist -> $HTTP_CODE"; exit 1; }

echo "6. Checking /smartlife-projection-demo -> 200..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "https://$SITE_NAME/smartlife-projection-demo")
[ "$HTTP_CODE" = "200" ] && echo "OK: /smartlife-projection-demo -> 200" || { echo "FAIL: /smartlife-projection-demo -> $HTTP_CODE"; exit 1; }

echo "7. Checking /smartlife-checkout-demo -> 200..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "https://$SITE_NAME/smartlife-checkout-demo")
[ "$HTTP_CODE" = "200" ] && echo "OK: /smartlife-checkout-demo -> 200" || { echo "FAIL: /smartlife-checkout-demo -> $HTTP_CODE"; exit 1; }

echo "8. Checking /smartlife-support-demo -> 200..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "https://$SITE_NAME/smartlife-support-demo")
[ "$HTTP_CODE" = "200" ] && echo "OK: /smartlife-support-demo -> 200" || { echo "FAIL: /smartlife-support-demo -> $HTTP_CODE"; exit 1; }

echo "9. Checking demo safety notice text on landing..."
PAGE_CONTENT=$(curl -s "https://$SITE_NAME/smartlife-flexi-demo")
echo "$PAGE_CONTENT" | grep -q "Prototype environment" && echo "OK: Demo notice present on landing" || { echo "FAIL: Demo notice missing"; exit 1; }
echo "$PAGE_CONTENT" | grep -q "real NSSF member data" && echo "OK: Demo safety text found" || { echo "FAIL: Demo safety text missing"; exit 1; }

echo "10. Checking projection disclaimer on projection page..."
PROJ_CONTENT=$(curl -s "https://$SITE_NAME/smartlife-projection-demo")
echo "$PROJ_CONTENT" | grep -q "indicative for demo purposes" && echo "OK: Projection disclaimer present" || { echo "FAIL: Projection disclaimer missing"; exit 1; }

echo "11. Checking GTM container ID..."
HOME_CONTENT=$(curl -s "https://$SITE_NAME")
echo "$HOME_CONTENT" | grep -q "GTM-PZRV3MQL" && echo "OK: GTM-PZRV3MQL present" || echo "NOTE: GTM-PZRV3MQL not found — ensure GTM snippet is in base template"

echo "12. Checking Helpdesk..."
curl -fsSI "https://$SITE_NAME/helpdesk/home" >/dev/null && echo "OK: Helpdesk responds" || echo "NOTE: Helpdesk not responding"

echo "13. Checking Cloudflare..."
curl -fsSI "https://$SITE_NAME" | grep -qi "server: cloudflare" && echo "OK: Cloudflare is active" || echo "NOTE: Cloudflare header not detected"

echo ""
echo "Smoke tests completed successfully."
