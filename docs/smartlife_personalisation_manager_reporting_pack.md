# SmartLife Flexi — Personalisation Manager Reporting Pack

This diagnostic reporting pack is designed for the SmartLife Personalisation Manager and Growth Team to optimize onboarding journeys, communications, and staff queues.

---

## 1. Acquisition Quality and Campaign Performance
- **Business Question**: Which advertising campaigns are producing actual savers (not just sign-up traffic)?
- **Action**: Pause campaigns showing low final conversion rates despite high traffic.
- **Recommended Chart Type**: Multi-Axis Bar & Line Chart.
- **Data Source**: `SmartLife Demo Lead` linked to `SmartLife Contribution Intent`
- **Formula**: `Conversion Rate = (Leads from Campaign X with Completed Payment) / (Leads from Campaign X) * 100`
- **Filters**: Campaign source, medium, date range
- **Alert Threshold**: Campaign conversion rate drops below 10%.
- **Privacy Risk**: Low (data aggregated by campaign).
- **Next Best Action**: Reallocate ad budget to the highest converting sources.

---

## 2. Journey Diagnostics and Funnel Dropoff
- **Business Question**: What onboarding steps act as dropoff barriers?
- **Action**: Refine steps with high dropout rates (e.g. projection calculator adjustments).
- **Recommended Chart Type**: Funnel Chart.
- **Data Source**: `SmartLife Demo Lead` (using step markers)
- **Formula**: `Dropoff % = (Leads exiting on Step X) / (Leads entering Step X) * 100`
- **Filters**: Segment, device type
- **Alert Threshold**: Dropoff exceeds 20% on any step.
- **Privacy Risk**: Low.
- **Next Best Action**: Run usability checks on mobile devices.

---

## 3. Segment and Life-Stage Mix
- **Business Question**: What goals do diaspora vs informal sector savers prioritize?
- **Action**: Adjust email templates to emphasize education vs business capital depending on the segment's goals.
- **Recommended Chart Type**: Stacked Column Chart.
- **Data Source**: `SmartLife Demo Lead`
- **Formula**: Pivot count by `saver_type` and `savings_goal`.
- **Filters**: Goal category, age band
- **Alert Threshold**: None (demographic mix indicators).
- **Privacy Risk**: Low.
- **Next Best Action**: Custom target newsletters for segments showing low engagement.

---

## 4. Onboarding Nursery and Incomplete Journeys
- **Business Question**: How many users abandoned onboarding on Step 2 (Personal Details) or Step 4 (Plan Setup)?
- **Action**: Assign these incomplete profiles to the staff queue for assisted completion.
- **Recommended Chart Type**: Line Trend Chart (daily counts).
- **Data Source**: `SmartLife Demo Lead`
- **Formula**: `Count(name) where lead_status = "Incomplete" and modification_date > 24 hours ago`
- **Filters**: Segment, preferred contact channel
- **Alert Threshold**: Incomplete pool count > 150.
- **Privacy Risk**: Medium (leads to staff queue access).
- **Next Best Action**: Dispatched automated checkout abandoned reminders.

---

## 5. Communication and Template Performance
- **Business Question**: Which email/SMS reminder templates yield the highest payment recovery?
- **Action**: Template performance should initially use send, simulated, failed and suppressed counts. Open-rate and click-through metrics should be added later only after tagged links, event tracking and approved measurement instrumentation are implemented.
- **Recommended Chart Type**: Grouped Column.
- **Data Source**: `SmartLife Communication Log` linked to `SmartLife Contribution Intent`
- **Formula**: `Recovery Rate = (Completed Intents within 48h of template receipt) / (Total template dispatches) * 100`
- **Filters**: Template name, delivery channel
- **Alert Threshold**: Template conversion drops below 5%.
- **Privacy Risk**: Low.
- **Next Best Action**: Conduct A/B testing on subject lines.

---

## 6. Payment Recovery Pool
- **Business Question**: What is the value of unpaid contribution drafts we can recover?
- **Action**: Run targeted SMS outreach to users with pending mobile money checkout requests.
- **Recommended Chart Type**: Stacked Bar (amount by duration).
- **Data Source**: `SmartLife Contribution Intent`
- **Formula**: `Sum(contribution_amount) where payment_status = "Pending" or "Draft"`
- **Filters**: Payment method, age band
- **Alert Threshold**: Recovery pool exceeds UGX 50,000,000.
- **Privacy Risk**: Low.
- **Next Best Action**: Trigger mobile money callback checks.

---

## 7. Staff Operational Throughput
- **Business Question**: Are support agents attending to follow-up queues in a timely manner?
- **Action**: Re-distribute workload to active staff members.
- **Recommended Chart Type**: Horizontal Columns (overdue count by staff).
- **Data Source**: `SmartLife Demo Lead`
- **Formula**: `Count(name) where next_follow_up_on < current_date`
- **Filters**: Staff assigned
- **Alert Threshold**: Single staff member has > 25 overdue tasks.
- **Privacy Risk**: Medium (staff names visible).
- **Next Best Action**: Support manager reassigns leads.

---

## 8. Support Resolution Trend
- **Business Question**: What technical issues are blocking onboarding completions?
- **Action**: Raise tickets to engineering for recurring payment failures.
- **Recommended Chart Type**: Area Chart.
- **Data Source**: `SmartLife Support Request`
- **Formula**: `Resolution Rate = (Closed tickets) / (Total tickets created) * 100`
- **Filters**: Topic category, priority
- **Alert Threshold**: Unresolved support queue grows by > 20% week-over-week.
- **Privacy Risk**: Low.
- **Next Best Action**: Allocate more agents to payment troubleshooting category.

---

## 9. Data Quality and Privacy Compliance
- **Business Question**: Are we maintaining zero PII leaks on our dashboards?
- **Action**: Flag filter attributes or logs violating mask rules.
- **Recommended Chart Type**: Compliance Scorecard.
- **Data Source**: System logs / Whitelist variables.
- **Formula**: `Score = (Compliant APIs / Total APIs) * 100`
- **Filters**: None
- **Alert Threshold**: Compliance score drops below 100% (leads to automatic system lockdown).
- **Privacy Risk**: Low.
- **Next Best Action**: Rebuild whitelist and strip non-allowed parameters from analytic helpers.
