# NSSF SmartLife Flexi — Staff User Guide

This guide is for Personalisation Team support staff triaging voluntary onboarding leads.

---

## 1. Staff Views Overview

### Masked Queue (`/smartlife-staff-queue`)
- **Purpose**: Operational dashboard displaying lead priorities.
- **Masking Rules**: Customer phone numbers and email addresses are masked (`070****545`, `ro***@domain.com`). No authenticated role is required.

### Full PII View (`/smartlife-staff-queue-full`)
- **Purpose**: Details view for authorized support team members.
- **Role Guard**: Requires `SmartLife Personalisation Team` role to access. Shows unmasked member names, phones, and emails.

---

## 2. Managing Triage Workflows

- **Assigning Leads**: Open a lead inside `/smartlife-staff-queue-full`. Choose the assignment option to allocate the lead reference to your user.
- **Updating Follow-Up Status**: Record progress (e.g. Call completed, callback requested) using the Follow-Up Outcome and Staff Notes fields.
- **Triggering Communications**: Choose templates (Welcome details, incomplete checkout reminders) to draft and send SMS/emails via the messaging panel.
- **Customer Support**: Track and resolve incoming support requests under the `/smartlife-support-demo` queues.

---

## 3. Privacy Policy & PII Obligations
- **Authorized Access Only**: Never access full queues from public or untrusted terminals.
- **Data Sharing**: Never export or copy raw phone numbers, NINs, or DOBs into non-secure tools.
- **Consent Respect**: Verify that the lead's `consent_to_contact` flag is checked before executing any telephone follow-ups or sending manual messages.
