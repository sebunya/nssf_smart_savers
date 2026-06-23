# SmartLife Demo Seed Data Plan

This plan outlines the safety protocols, fictional scenarios, and execution commands to seed and clear controlled fictional demo data for visual UAT validation and personalization manager walkthroughs.

## Purpose & Scope
The goal of this data pack is to make the NSSF SmartLife Flexi system feel realistic and institutional during UAT, staff reviews, and board presentations, avoiding empty states. The demo data models onboarding adoption, channel distribution, drop-offs, and service recovery.

## Fictional Data Safety Rules

Every seed record is strictly fictional and explicitly marked.
- **Deterministic Identifiers**: Leads use `DEMO-SMARTLIFE-001` through `DEMO-SMARTLIFE-010`. intents use `SL-INTENT-DEMO-SMARTLIFE-xxx`. support requests use `SL-SUPPORT-DEMO-SMARTLIFE-xxx`.
- **Fictional Wording**: Visible notes and labels contain `SmartLife UAT demo data` or `Sample UAT record`.
- **No PII**: All emails use `@example.test`. All phone numbers use mock formatting (e.g. `+256700000001`). No real Ugandan names, real NINs, real banking accounts, or live provider references are included.
- **Production Guardrails**: Seed scripts are not registered in `hooks.py`, migration patches, or page-load triggers. They must be explicitly executed by the operator via the command-line interface.

## 10 Scenario Personas

| Scenario ID | Name / Segment | Stage / Status | Goal / Initial Deposit | Comms Logs | Support Request | Key Demo Diagnostic |
|---|---|---|---|---|---|---|
| `001` | Demo Saver 001<br>(Salaried) | Onboarded<br>Payment Completed | Education Fund<br>UGX 250,000 | 1 Sent | None | Board success case; fully completed journey. |
| `002` | Demo Saver 002<br>(Salaried) | Checkout Started<br>Payment Pending | Retirement Fund<br>UGX 500,000 | 1 Sent | None | Payment recovery scenario. |
| `003` | Demo Saver 003<br>(Diaspora) | Onboarded<br>Payment Completed | Land Fund<br>UGX 2,000,000 | 1 Sent | 1 Resolved | Diaspora segment; international card checkout. |
| `004` | Demo Saver 004<br>(Informal) | Profile Incomplete<br>New | Business Fund<br>UGX 50,000 | 1 Sent | None | Onboarding drop-off at Step 1. |
| `005` | Demo Saver 005<br>(Salaried) | Projection Viewed<br>Warm | Retirement Fund<br>UGX 150,000 | 1 Sent | None | Projection-to-checkout leakage case. |
| `006` | Demo Saver 006<br>(Informal) | Checkout Started<br>Checkout Started | Education Fund<br>UGX 200,000 | 1 Sent | 1 In Progress | Payment friction case (mobile money failed). |
| `007` | Demo Saver 007<br>(Informal) | Goal Selected<br>Staff Follow-up Req. | Land Fund<br>UGX 300,000 | 1 Sent | 1 Assigned | Staff-assisted lead needing priority follow-up. |
| `008` | Demo Saver 008<br>(Salaried) | Onboarded<br>Contacted | Retirement Fund<br>UGX 400,000 | 1 Sent | 1 New | Product comprehension query (existing member status). |
| `009` | Demo Saver 009<br>(Salaried) | Onboarded<br>Contacted | Education Fund<br>UGX 300,000 | 1 Skipped | None | Consent suppression (no communications sent). |
| `010` | Demo Saver 010<br>(Informal) | Onboarded<br>Dormant | Business Fund<br>UGX 100,000 | 1 Sent | None | Retention and dormancy reactivation scenario. |

## Expected Aggregate Metrics

When seeded, the aggregate dashboards and charts will reflect the following distribution:
- **Onboarding Starts**: 10
- **Completed Onboarding**: 7 (Scenario 1, 3, 5, 8, 9, 10; Scenario 7 reached Goal)
- **Projection Calculated**: 6 (Scenario 1, 2, 3, 5, 6, 10; Scenario 7 assisted)
- **Checkout Initiated**: 5 (Scenario 1, 2, 3, 6, 10)
- **Contributions Initiated**: 5
- **Completed Payments**: 2 (Scenario 1, 3)
- **Pending/Failed Payments**: 2 (Scenario 2 pending, Scenario 6 failed)
- **Support Requests**: 4 (Scenario 3, 6, 7, 8)
- **Consent Suppressed (Skipped Comms)**: 1 (Scenario 9)
- **Dormancy Risk**: 1 (Scenario 10)

## Operator Runbook

A helper script is provided at `scripts/seed_smartlife_demo_data.sh`. It requires explicit arguments and does not run automatically.

### 1. Preview Scenario Definitions
```bash
bash scripts/seed_smartlife_demo_data.sh preview
```

### 2. Seed Demo Data
```bash
bash scripts/seed_smartlife_demo_data.sh seed
```

### 3. Clear Demo Data
```bash
bash scripts/seed_smartlife_demo_data.sh clear
```

## Privacy & Small-Count Suppression
Because this seed pack generates exactly 10 records, certain segment charts will show cohort counts under 5. This is normal for visual validation. In live production environments, a cohort threshold of 5 is enforced to prevent exposing individual behavior in reporting dashboards.

## Status Summary
- **Phase 8 Release Pack**: `Phase 8 release pack verified / server validation pending`
- **UI/UX Acceptance**: `UI/UX executive professionalisation complete / server browser validation pending`
- **Reporting Strategy**: `Reporting enhancement blueprint complete / implementation pending`
- **Demo Seed status**: `Demo seed and NSSF brand cleanup complete / server validation pending`
