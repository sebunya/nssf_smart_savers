# SmartLife Flexi — Board Reporting Pack

This reporting pack is designed for the NSSF Uganda Board and Executive Committee to evaluate system growth, adoption patterns, operational friction, and security compliance.

---

## 1. Executive Performance Scorecard
- **Headline Cards**: Onboarding Starts, Completed Profiles, Active Plans, Total Intents, Payment Success Rate, Open Support Queries, Privacy Audit Status.
- **Board Question**: What is the overall health of the SmartLife project?
- **Why It Matters**: Gives a high-level view of customer growth and system errors.
- **Data Source**: `SmartLife Demo Lead`, `SmartLife Contribution Intent`, `SmartLife Support Request`
- **Formula**: Cumulative sum of records created within period.
- **Recommended Chart Type**: Large KPI Number Cards.
- **Filters**: Date range
- **Decision Signal**: Compares target conversion metrics with actual performance.
- **RAG Interpretation**: 
  - 🟢 **Green**: Onboarding conversion > 70%, Payment success > 90%, Open support requests < 50.
  - 🟡 **Amber**: Conversion 50%-70%, Success 75%-90%.
  - 🔴 **Red**: Conversion < 50% or Payment success < 75% (requires emergency developer audit).
- **Privacy Classification**: Public within NSSF Board.
- **Owner**: Product Director
- **Action**: Review callback latency with the payment team.

---

## 2. Onboarding Conversion Funnel
- **Board Question**: At which step are customers dropping out during onboarding?
- **Why It Matters**: pinpoints form friction or calculation confusion.
- **Data Source**: `SmartLife Demo Lead`
- **Formula**: Stage counts (Started, Details, Goal, Plan, Projection, Checkout) divided by Starts.
- **Recommended Chart Type**: Horizontal Funnel Chart.
- **Filters**: Saver segment
- **Decision Signal**: Identifies step dropout rates.
- **RAG Interpretation**:
  - 🟢 **Green**: Progression dropoff less than 10% per step.
  - 🔴 **Red**: Dropoff greater than 20% on a single step.
- **Privacy Classification**: Restrained (aggregated counts).
- **Owner**: Lead UX Designer
- **Action**: Simplify field requirements on high-dropoff steps.

---

## 3. Segment Adoption Mix
- **Board Question**: Are we successfully attracting informal savers and the diaspora?
- **Why It Matters**: Verifies if the project is reaching target underserved groups.
- **Data Source**: `SmartLife Demo Lead`
- **Formula**: Group by `saver_type`.
- **Recommended Chart Type**: Donut Chart.
- **Filters**: Month
- **Decision Signal**: Adoption ratio compared to NSSF strategic targets.
- **RAG Interpretation**:
  - 🟢 **Green**: Diaspora and Informal sectors combined exceed 40% of the mix.
  - 🔴 **Red**: Combined mix less than 20% (indicates campaigns are hitting existing members only).
- **Privacy Classification**: Restrained.
- **Owner**: Head of Growth Marketing
- **Action**: Reallocate ad spend towards diaspora-specific newsletters and informal forums.

---

## 4. Contribution and Payment Health
- **Board Question**: Are users completing payment setup, and are sandbox/live systems functioning?
- **Why It Matters**: Monitors cash activation and gateway processing reliability.
- **Data Source**: `SmartLife Contribution Intent`
- **Formula**: Group counts by `payment_status`.
- **Recommended Chart Type**: Stacked Horizontal Bar.
- **Filters**: Payment channel
- **Decision Signal**: Ratio of completed payments to drafts/failed.
- **RAG Interpretation**:
  - 🟢 **Green**: Completed payments > 90%.
  - 🔴 **Red**: Failed payments exceed 10% (system failure flag).
- **Privacy Classification**: Confidential.
- **Owner**: Head of Finance Integration
- **Action**: Reconcile sandbox tracking IDs against the gateway gateway log.

---

## 5. Account Activation Quality
- **Board Question**: Are signed-up users actually saving, or are they dormant?
- **Why It Matters**: Prevents reporting inflated sign-up counts without actual savings deposit behaviour.
- **Data Source**: `SmartLife Demo Lead` linked to `SmartLife Contribution Intent`
- **Formula**: Leads with Completed Intents vs Leads with no Intents.
- **Recommended Chart Type**: Side-by-side Columns.
- **Filters**: Date range
- **Decision Signal**: Percentage of active savers.
- **RAG Interpretation**:
  - 🟢 **Green**: > 60% of accounts have made at least one contribution.
  - 🔴 **Red**: < 30% activation rate (leads are signing up but never depositing).
- **Privacy Classification**: Restrained.
- **Owner**: Personalisation Manager
- **Action**: Trigger automatic reminder messaging schedules.

---

## 6. Communication and Consent Health
- **Board Question**: Is the personalization system operating legally and within privacy rules?
- **Why It Matters**: Ensures legal compliance with data privacy regulations.
- **Data Source**: `SmartLife Communication Log`
- **Formula**: Delivery states (Sent, Suppressed, Consent Missing) by channel.
- **Recommended Chart Type**: Stacked Composition Bar.
- **Filters**: Channel (SMS vs Email)
- **Decision Signal**: Count of consent suppressions.
- **RAG Interpretation**:
  - 🟢 **Green**: 0 messages dispatched without explicit consent.
  - 🔴 **Red**: Any message sent to a user marked as consent-withdrawn (automatic compliance audit).
- **Privacy Classification**: Strictly Confidential.
- **Owner**: NSSF Data Protection Officer (DPO)
- **Action**: Halt automated queue dispatches and audit log triggers.

---

## 7. Customer Friction Mix
- **Board Question**: What queries are users raising, and where is the product confusing?
- **Why It Matters**: Highlights support issues and customer pain points.
- **Data Source**: `SmartLife Support Request`
- **Formula**: Group by `support_category`.
- **Recommended Chart Type**: Vertical Columns.
- **Filters**: Lead temperature
- **Decision Signal**: Ratio of payment support to general joining help.
- **RAG Interpretation**:
  - 🟢 **Green**: Total support tickets < 5% of starts.
  - 🔴 **Red**: Ticket rate > 15% (indicates system friction).
- **Privacy Classification**: Restrained.
- **Owner**: Support Manager
- **Action**: Update step copy and FAQ files on the checkout page.

---

## 8. Deployment Readiness and Risk
- **Board Question**: Is the system technically ready to transition to production?
- **Why It Matters**: Operational risk assessment before public release.
- **Data Source**: `SmartLife Production Checklist` / System variables.
- **Formula**: Number of completed setup items / Total setup items.
- **Recommended Chart Type**: Progress Ring / Checkmark Table.
- **Filters**: None
- **Decision Signal**: Open readiness configuration keys.
- **RAG Interpretation**:
  - 🟢 **Green**: All checklists completed, smoke tests passed, and DPO sign-off recorded.
  - 🔴 **Red**: DPO sign-off missing or test failures present.
- **Privacy Classification**: Public within NSSF Board.
- **Owner**: Release Manager
- **Action**: Block production merge until all gates are green.
