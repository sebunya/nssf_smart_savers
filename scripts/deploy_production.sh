#!/usr/bin/env bash
set -euo pipefail

BENCH_PATH="${BENCH_PATH:-/home/frappe/frappe-bench}"
SITE_NAME="${SITE_NAME:-nssf-smartlifeflexi.nile-gov-demo.com}"
APP_NAME="${APP_NAME:-nssf_smart_savers}"
APP_PATH="$BENCH_PATH/apps/$APP_NAME"

echo "Deploying $APP_NAME to $SITE_NAME"

if [ ! -d "$BENCH_PATH" ]; then
  echo "ERROR: Bench path not found: $BENCH_PATH"
  exit 1
fi

if [ ! -d "$APP_PATH" ]; then
  echo "ERROR: App path not found: $APP_PATH"
  exit 1
fi

cd "$APP_PATH"

echo "Current branch:"
git branch --show-current

echo "Current commit:"
git log --oneline -1

echo "Checking working tree..."
git status --short

if [ -n "$(git status --short)" ]; then
  echo "ERROR: Working tree is not clean. Commit or stash changes before deploying."
  exit 1
fi

echo "Fetching latest main..."
git fetch origin main
git checkout main
git pull --ff-only origin main

cd "$BENCH_PATH"

echo "Creating bench backup..."
bench --site "$SITE_NAME" backup --with-files

echo "Running migrations..."
bench --site "$SITE_NAME" migrate

echo "Building assets..."
bench build --app "$APP_NAME"

echo "Clearing cache..."
bench --site "$SITE_NAME" clear-cache
bench --site "$SITE_NAME" clear-website-cache

echo "Restarting services..."
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

echo "Running smoke tests..."
"$APP_PATH/scripts/smoke_test.sh"

echo "Deployment completed successfully."
