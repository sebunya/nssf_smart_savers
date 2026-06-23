# NSSF SmartLife Flexi — Demo Walkthrough Guide

This document details the user journey workflow through the SmartLife Flexi prototype.

---

## 1. Customer User Journey Narrative

### Step 1: Landing Page (`/smartlife-flexi-demo`)
- **What it shows**: The NSSF visual identity, voluntary saving values, goal selectors (Buy a home, Start a business, Education, Retirement, etc.), and saver types.
- **Data Captured**: `goal` and `saver_type` (saved in localStorage).

### Step 2: Onboarding Form (`/smartlife-self-serve`)
- **What it shows**: Form fields capturing contact info and birth parameters.
- **DOB Personalization**: Calculates client age band server-side based on provided Date of Birth. Excludes manual age entry.
- **Data Captured**: Name, Phone, Email, DOB, NIN, and Consent status.

### Step 3: Projections Calculator (`/smartlife-projection-demo`)
- **What it shows**: An interactive graph modeling target savings against weekly/monthly contribution plans.
- **Data Captured**: Contribution Amount, Frequency, Initial Deposit, and Income Source.

### Step 4: Checkout Demo (`/smartlife-checkout-demo`)
- **What it shows**: Onboarding plan summary and payment method selector (Mobile Money, Card, Bank Transfer, Demo Checkout).
- **Data Captured**: Payment Method and Status.

### Step 5: Thank-You page (`/smartlife-thank-you`)
- **What it shows**: Onboarding completion summary. URL parameters are sanitized to confirm zero PII leakage.

---

## 2. Personalisation Team (Staff Flow)

### Step 1: Public Masked Queue (`/smartlife-staff-queue`)
- **What it shows**: Onboarding leads grouped by temperatures (Hot, Warm, Cold).
- **PII Protection**: Phone numbers and emails are masked. Authenticated access is not required.

### Step 2: Full Queue (`/smartlife-staff-queue-full`)
- **What it shows**: Priority triage queue. Displays unmasked member names, phone numbers, emails, and DOBs.
- **Role Guard**: Blocked by a secure gate. Requires `SmartLife Personalisation Team` role to bypass.

### Step 3: Command Centre (`/smartlife-command-centre`)
- **What it shows**: Summary metric cards (Total Leads, Details Completed, Conversion Rate) and drop-off analysis. No customer-level PII or rows are accessible.
