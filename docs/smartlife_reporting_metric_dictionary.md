# SmartLife Flexi — Reporting Metric Dictionary

This document defines the metrics used across the NSSF SmartLife Flexi reporting packs.

---

## 1. Onboarding Completion Rate
- **Audience**: Board, Personalisation Manager
- **Business Question**: Are users completing the self-serve onboarding sequence?
- **Definition**: Percentage of onboarding starts that reach the confirmation step.
- **Formula**: `(Leads with status = "Completed") / (Total Leads Created) * 100`
- **Data Source**: `SmartLife Demo Lead`
- **Required Fields**: `lead_status`, `creation`
- **Filters**: Date range, Segment
- **Grain**: Daily/Monthly
- **Refresh Cadence**: Daily (cached)
- **PII Risk**: None (aggregated count)
- **Edge Cases**: Unfinished drop-off logs are counted as starts.
- **Interpretation**: A high rate (>70%) indicates a frictionless onboarding form.
- **Recommended Action**: If below 50%, evaluate Form step layouts.
- **Owner**: Growth Team Lead

---

## 2. Onboarding Starts
- **Audience**: Personalisation Manager
- **Business Question**: How many prospects are entering our funnel?
- **Definition**: Cumulative count of new lead records.
- **Formula**: `Count(name) where creation is within date range`
- **Data Source**: `SmartLife Demo Lead`
- **Required Fields**: `name`, `creation`
- **Filters**: Campaign source
- **Grain**: Hourly/Daily
- **Refresh Cadence**: Real-time
- **PII Risk**: None
- **Edge Cases**: Duplicate clicks create unique sessions.
- **Interpretation**: Measures campaign traffic volumes.
- **Recommended Action**: Optimize marketing channels if volume stalls.
- **Owner**: Digital Marketing Manager

---

## 3. Contribution Intent Count
- **Audience**: Board, Personalisation Manager
- **Business Question**: How many payment checkouts are initiated?
- **Definition**: Total number of contribution intents created.
- **Formula**: `Count(name) from Contribution Intent`
- **Data Source**: `SmartLife Contribution Intent`
- **Required Fields**: `name`, `payment_status`
- **Filters**: Payment method, segment
- **Grain**: Daily
- **Refresh Cadence**: Real-time
- **PII Risk**: None
- **Edge Cases**: Excludes dummy system-test records.
- **Interpretation**: Higher intent count shows strong user interest in saving.
- **Recommended Action**: Monitor payment channel distributions.
- **Owner**: Finance Operations Manager

---

## 4. Payment Success Rate
- **Audience**: Board, Personalisation Manager
- **Business Question**: Are payment checkouts completing successfully?
- **Definition**: Percentage of contribution intents that transition to Completed status.
- **Formula**: `(Intents with status = "Completed") / (Total Intents Created) * 100`
- **Data Source**: `SmartLife Contribution Intent`
- **Required Fields**: `payment_status`
- **Filters**: Payment method, currency
- **Grain**: Daily/Monthly
- **Refresh Cadence**: Hourly (cached)
- **PII Risk**: None
- **Edge Cases**: Does not include demo-mode simulation intents.
- **Interpretation**: Low success rate (<90%) points to gateway callback errors.
- **Recommended Action**: Review Pesapal adapter callback latency.
- **Owner**: Integrations Engineer

---

## 5. Delivery/Simulation Rate
- **Audience**: Personalisation Manager
- **Business Question**: Are campaign messages successfully sent or simulated?
- **Definition**: Percentage of communication logs marked as Sent or Simulated.
- **Formula**: `(Logs with status = "Sent" or "Simulated") / (Total Logs Created) * 100`
- **Data Source**: `SmartLife Communication Log`
- **Required Fields**: `message_status`
- **Filters**: Channel type, template name
- **Grain**: Daily
- **Refresh Cadence**: Hourly
- **PII Risk**: None
- **Edge Cases**: Excludes records suppressed due to lack of consent.
- **Interpretation**: Verifies provider connectivity and message dispatching.
- **Recommended Action**: Troubleshoot ZeptoMail or Phahapa logs if rate drops.
- **Owner**: System Administrator

---

## 6. Segment Mix
- **Audience**: Board
- **Business Question**: Are we reaching the target diaspora and informal sectors?
- **Definition**: Ratio of savers by segment.
- **Formula**: `Count(name) grouped by saver_type`
- **Data Source**: `SmartLife Demo Lead`
- **Required Fields**: `saver_type`
- **Filters**: Date range
- **Grain**: Monthly
- **Refresh Cadence**: Daily (cached)
- **PII Risk**: None
- **Edge Cases**: Leads with empty saver types are grouped into "Other".
- **Interpretation**: Shows if outreach is matching NSSF voluntary goals.
- **Recommended Action**: Adjust diaspora campaigns if mix falls below target.
- **Owner**: Product Strategy Lead

---

## 7. Overdue Follow-Up Count
- **Audience**: Personalisation Manager
- **Business Question**: Are staff follow-up queues backing up?
- **Definition**: Number of leads assigned to staff with follow-up dates in the past.
- **Formula**: `Count(name) where next_follow_up_on < current_date and lead_status = "Follow Up"`
- **Data Source**: `SmartLife Demo Lead`
- **Required Fields**: `next_follow_up_on`, `lead_status`, `assigned_staff`
- **Filters**: Assigned staff member
- **Grain**: Daily
- **Refresh Cadence**: Real-time
- **PII Risk**: Staff name visible to manager (no customer PII).
- **Edge Cases**: Completed follow-ups that were not updated in Desk.
- **Interpretation**: Measures staff operational throughput.
- **Recommended Action**: Reassign leads to active support agents.
- **Owner**: Support Operations Manager

---

## 8. Support Category Mix
- **Audience**: Personalisation Manager
- **Business Question**: What friction points block savers?
- **Definition**: Total support queries grouped by category.
- **Formula**: `Count(name) grouped by support_category`
- **Data Source**: `SmartLife Support Request`
- **Required Fields**: `support_category`
- **Filters**: Status
- **Grain**: Monthly
- **Refresh Cadence**: Hourly
- **PII Risk**: None
- **Edge Cases**: Categorized manually if default logic is unclear.
- **Interpretation**: Identifies top product challenges (e.g. payment issues).
- **Recommended Action**: Rewrite copy or fix steps with highest friction categories.
- **Owner**: Customer Experience Manager

---

## 9. Data Completeness Score
- **Audience**: Governance, Quality Assurance
- **Business Question**: Are mandatory reporting profiles fully populated?
- **Definition**: Percentage of leads with complete, non-null fields for key attributes.
- **Formula**: `(Leads with segment, goal, consent, channel non-null) / (Total Leads) * 100`
- **Data Source**: `SmartLife Demo Lead`
- **Required Fields**: `saver_type`, `savings_goal`, `consent_to_contact`, `preferred_contact_channel`
- **Filters**: Date range
- **Grain**: Monthly
- **Refresh Cadence**: Daily
- **PII Risk**: None
- **Edge Cases**: Missing values default to null.
- **Interpretation**: High score (>95%) indicates high-quality lead capture data.
- **Recommended Action**: Make fields mandatory on forms if score drops.
- **Owner**: Compliance Officer
