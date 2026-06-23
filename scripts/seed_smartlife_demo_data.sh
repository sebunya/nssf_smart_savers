#!/usr/bin/env bash
set -euo pipefail

# Helper script for NSSF SmartLife Flexi Demo/UAT Seed Data operations.
# Strictly for prototype/UAT validation contexts only.

COMMAND="${1:-}"

print_usage() {
  echo "Usage: bash scripts/seed_smartlife_demo_data.sh [preview|seed|clear]"
  echo ""
  echo "Commands:"
  echo "  preview  Show definitions of the 10 fictional UAT scenarios (read-only)"
  echo "  seed     Idempotently write exactly 10 fictional scenarios to the database"
  echo "  clear    Safely delete the 10 fictional scenarios and linked demo log records"
  echo ""
  echo "Requires bench to be available on PATH and to be run in the active site directory."
}

if [ -z "$COMMAND" ]; then
  print_usage
  exit 1
fi

case "$COMMAND" in
  preview)
    echo "Retrieving fictional UAT scenarios preview..."
    bench execute nssf_smart_savers.demo_data.smartlife_demo_seed.get_demo_seed_preview
    ;;
  seed)
    echo "Executing idempotent seed of 10 fictional scenarios..."
    bench execute nssf_smart_savers.demo_data.smartlife_demo_seed.seed_demo_data
    ;;
  clear)
    echo "Clearing all fictional demo seed records..."
    bench execute nssf_smart_savers.demo_data.smartlife_demo_seed.clear_demo_data
    ;;
  *)
    echo "ERROR: Unknown command '$COMMAND'"
    print_usage
    exit 1
    ;;
esac
