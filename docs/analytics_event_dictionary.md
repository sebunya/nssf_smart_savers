# Analytics Event Dictionary — SmartLife Flexi

GTM Container: GTM-PZRV3MQL

## Events

| Event Name | Trigger | Key Params |
|-----------|---------|-----------|
| sl_demo_view | Page load on any demo page | journey_type, step_name |
| sl_segment_selected | User clicks segment card | segment |
| sl_goal_selected | User clicks goal card | goal_category, segment |
| sl_projection_viewed | Projection calculated | frequency, period_band |
| sl_plan_generated | Personalised plan shown | segment, goal_category, frequency |
| sl_staff_assist_started | Staff session submitted | segment, goal_category |
| sl_demo_submit | Journey completed | journey_type, goal_category, frequency, completion_status |
| sl_payment_simulated | Payment simulation run | payment_status, frequency, goal_category |
| sl_support_requested | Support form submitted | journey_type, step_name |
| sl_dropoff_detected | User exits dirty form | dropoff_step, journey_type |

## Allowed Params (ALLOWED_PARAMS)
- journey_type: self_serve | staff_assist | projection | checkout | support
- segment: existing_member | new_voluntary | diaspora | civil_servant | formal_sector | informal_sector | parent_guardian | staff_assisted_prospect
- goal_category: marriage | vacation | homeownership | school_fees | wedding | emergencies | education | avoiding_debt | investment | financial_security | job_loss_cushion | car | retirement | financial_independence | other
- frequency: daily | weekly | monthly | quarterly | semi-annually | annually
- period_band: 1y | 1-3y | 3-5y | 5-10y | 10y+
- target_band: <500k | 500k-2m | 2m-10m | 10m-50m | 50m+
- country_band: uganda | east_africa | diaspora | unknown
- step_name: any step identifier string (max 100 chars)
- staff_assisted: yes | no
- payment_status: Pending | Initiated | Success | Failed | Cancelled
- completion_status: complete | partial | abandoned
- dropoff_step: step identifier
- lead_stage: New | Interested | Plan Shown | Follow-up | Converted | Lost

## PII Policy
- **NEVER** include NIN, phone, email, name, or any identifying data in analytics events
- All params are passed through `SmartLifeAnalytics.sanitise()` before pushing to dataLayer
- Max 100 chars per param value
