# SmartLife Flexi — Presenter Demo Script

This document details the step-by-step walkthrough for demonstrating the NSSF SmartLife Flexi Voluntary Saving Growth System. Presenters should follow this sequence to showcase the system features to stakeholders, managers, or auditors.

---

## Demo Step Sequence

### 1. Landing Page (`/smartlife-flexi-demo`)
- **Action**: Open the browser to `/smartlife-flexi-demo`.
- **Purpose**: Showcase the initial landing experience. Highlight the goal selection (e.g., Education, Retirement, Business, Land), selection of saver type (Salaried vs. Informal), and the professional NSSF brand styling (NSSF Blue and Yellow color theme).
- **Captured Data**: Temporary frontend goal selection and saver type selection.

### 2. Self-Serve Onboarding (`/smartlife-self-serve`)
- **Action**: Click "Get Started" to navigate to `/smartlife-self-serve`.
- **Purpose**: Show the customer self-serve flow. Fill in mock personal details (First Name, Last Name, Email, Phone, and Date of Birth). Enter a target savings goal and contribution amount.
- **Captured Data**: Lead details initialized, but not finalized.

### 3. Date of Birth Personalisation
- **Action**: Select a Date of Birth on the onboarding form and observe the age-band response.
- **Purpose**: Demonstrate server-side personalization. Point out that the system computes the saver's age band on the server backend rather than asking the user to enter their age manually.
- **Captured Data**: Birth month, birth year, and computed age band.

### 4. Projection Engine (`/smartlife-projection-demo`)
- **Action**: Proceed to the projection screen.
- **Purpose**: Explain the compound interest and savings growth projection system. Show the interactive savings projection chart or timeline showing how contribution amounts match up against target goals over time.
- **Captured Data**: Onboarding simulation parameters.

### 5. Checkout (`/smartlife-checkout-demo`)
- **Action**: Proceed to checkout at `/smartlife-checkout-demo`.
- **Purpose**: Show the plan summary, frequency, and payment method selector (Mobile Money, Card, etc.). Emphasize the clear "Sandbox / Demo Mode" warning banner, showing that transactions are not processed live.
- **Captured Data**: Payment method, contribution intent draft.

### 6. Thank You (`/smartlife-thank-you`)
- **Action**: Complete the checkout process to reach the confirmation page.
- **Purpose**: Show the onboarding completion screen. Summarize the user's choices, display their assigned lead status, and provide the next steps.
- **Captured Data**: Lead conversion marker, final session state locked.

### 7. Staff-Assisted Flow (`/smartlife-staff-assist`)
- **Action**: Open `/smartlife-staff-assist` in a new tab or window.
- **Purpose**: Demonstrate how an NSSF agent/staff member can assist an offline customer. Show the agent filling in the customer's details and managing the onboarding steps on their behalf.
- **Captured Data**: Onboarding record created with `created_by_channel` marked as "Staff-Assisted".

### 8. Staff Queue Masked View (`/smartlife-staff-queue`)
- **Action**: Navigate to `/smartlife-staff-queue`.
- **Purpose**: Show the queue view that NSSF staff use to prioritize leads. Highlight that names, email addresses, and phone numbers are masked or partially hidden to protect privacy.
- **Captured Data**: Lead metrics and follow-up activities.

### 9. Personalisation Team Full PII View (`/smartlife-staff-queue-full`)
- **Action**: Navigate to `/smartlife-staff-queue-full`.
- **Purpose**: Show that access to the full, unmasked PII (names, raw emails, phone numbers) is restricted by a strict Frappe role gate (`SmartLife Personalisation Team` role). Attempt to access it without authorization to show the access denial.
- **Captured Data**: Full customer contact list (authorized access only).

### 10. Contribution Intent Sandbox Demo
- **Action**: Select a mock payment inside the checkout screen and view the resulting `SmartLife Contribution Intent` document status in the Desk (for administrators).
- **Purpose**: Demonstrate integration with the Pesapal sandbox gateway. Show the transition of status from Draft to Checkout Started, and simulate status callbacks.
- **Captured Data**: Merchant references, tracking IDs, and callback statuses.

### 11. Communications & Suppression (`/smartlife-messaging-demo`)
- **Action**: Open `/smartlife-messaging-demo`.
- **Purpose**: Demonstrate how communication templates are selected and sent. Explain the opt-in/consent enforcement rules and how all communications are recorded under `SmartLife Communication Log` with masked recipient logs.
- **Captured Data**: Message templates, opt-in status, and logs.

### 12. Command Centre Dashboard (`/smartlife-command-centre`)
- **Action**: Navigate to `/smartlife-command-centre`.
- **Purpose**: Present the operational dashboard. Show real-time charts including conversion rates, funnel dropoffs, lead demographics, and campaign tracking. Crucially, show that NO PII is loaded, calculated, or shown in the charts.
- **Captured Data**: Aggregate metrics only.

### 13. Support & Helpdesk Flow (`/smartlife-support-demo`)
- **Action**: Open `/smartlife-support-demo`, fill out a support request, and submit.
- **Purpose**: Demonstrate how members submit questions. Show how support requests are triaged under the `SmartLife Support Request` DocType, categorized, and assigned to agent queues.
- **Captured Data**: Sanitized description, categorization, and assignment logs.

### 14. Privacy & PII Hardening Demo
- **Action**: Explain the underlying protection mechanisms.
- **Purpose**: Detail the `analytics_helper.js` script with its client-side PII block list. Highlight the strict API parameters whitelist (`ALLOWED_PARAMS`) and backend decorators that block guest requests on sensitive endpoints.
- **Captured Data**: None (security architecture demonstration).

### 15. What's Next / Production Transition
- **Action**: Review the final transition slide or notes.
- **Purpose**: Explain the checklist of requirements for the live launch, focusing on system configuration keys, HTTPS, and obtaining the NSSF Data Protection Officer (DPO) sign-off.
