#!/usr/bin/env bash
set -euo pipefail

SITE_NAME="${SITE_NAME:-nssf-smartlifeflexi.nile-gov-demo.com}"
BENCH_PATH="${BENCH_PATH:-/home/frappe/frappe-bench}"
APP_NAME="${APP_NAME:-nssf_smart_savers}"

echo "Running smoke tests for $SITE_NAME"

cd "$BENCH_PATH"

echo "1. Checking installed apps..."
bench --site "$SITE_NAME" list-apps | grep -q "$APP_NAME"
echo "OK: $APP_NAME is installed"

echo "2. Checking homepage..."
curl -fsSI "https://$SITE_NAME" >/dev/null
echo "OK: Homepage responds"

echo "3. Checking Helpdesk..."
curl -fsSI "https://$SITE_NAME/helpdesk/home" >/dev/null
echo "OK: Helpdesk responds"

echo "4. Checking Cloudflare..."
curl -fsSI "https://$SITE_NAME" | grep -qi "server: cloudflare"
echo "OK: Cloudflare is active"

echo "5. Optional future SmartLife route..."
if curl -fsSI "https://$SITE_NAME/smartlife-flexi-demo" >/dev/null 2>&1; then
  echo "OK: /smartlife-flexi-demo responds"
else
  echo "NOTE: /smartlife-flexi-demo not live yet. Expected before feature build."
fi

echo "Smoke tests completed."
