/**
 * SmartLife Flexi — Analytics Helper
 * Wraps GTM dataLayer pushes with a strict PII block-list.
 * Raw personal data MUST NEVER reach GTM, GA4, Clarity, or any analytics endpoint.
 */
(function(window) {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  /* Explicit PII block-list — keys that must never reach analytics */
  var PII_KEYS = [
    'name','first_name','last_name','full_name','fname','lname',
    'phone','phone_number','primary_phone','alt_phone','mobile','tel',
    'email','email_address',
    'nin','national_id','passport','member_number','nssf_number',
    'dob','date_of_birth','birth_date','birthday','birthday_day','birthday_month',
    'age_years','exact_age','age',
    'otp','pin','password','secret',
    'account','bank_account','card','payment_ref','transaction_id',
    'address','location','street','postcode','zip'
  ];

  /* Allow-list of keys that ARE safe to send to analytics */
  var ALLOWED_KEYS = [
    'event','demo_environment',
    'anonymous_session_id','route','step_name','event_name',
    'saver_type','savings_goal','contribution_frequency','amount_band',
    'age_band','gender_category','country_category',
    'source_of_income_category','industry_category',
    'consent_status','conversion_stage',
    'segment','goal_category','goal','segment_category',
    'payment_status','dropoff_step','plan_type'
  ];

  function isPiiKey(k) {
    var lower = String(k).toLowerCase().replace(/[\-_\s]/g,'');
    return PII_KEYS.some(function(p){return lower.indexOf(p.replace(/[\-_]/g,''))!==-1;});
  }

  function sanitise(params) {
    if (!params || typeof params !== 'object') return {};
    var safe = {};
    Object.keys(params).forEach(function(k) {
      if (isPiiKey(k)) {
        console.warn('[SLAnalytics] Blocked PII key from analytics:', k);
        return;
      }
      /* Also block values that look like phone numbers, emails, or long identifiers */
      var v = String(params[k] || '');
      if (/\+?[0-9]{9,}/.test(v) || /@/.test(v) || /CM\d{7}/i.test(v)) {
        console.warn('[SLAnalytics] Blocked PII-like value for key:', k);
        return;
      }
      safe[k] = v.slice(0, 120);
    });
    return safe;
  }

  function safePush(eventName, params) {
    try {
      var payload = Object.assign({ event: String(eventName||'').slice(0,80) }, sanitise(params));
      payload.demo_environment = 'true';
      window.dataLayer.push(payload);
    } catch(e) {
      /* Analytics must never break the page */
    }
  }

  /* Also expose as SLAnalytics so inline code can push safely */
  window.SLAnalytics = { push: function(p){ safePush(p&&p.event||'sl_event', p); } };

  window.SmartLifeAnalytics = {
    push: function(eventName, params) { safePush(eventName, params); },
    demoView: function(p) { safePush('sl_demo_view', p); },
    segmentSelected: function(segment) { safePush('sl_segment_selected', { saver_type: segment }); },
    goalSelected: function(goal, segment) { safePush('sl_goal_selected', { savings_goal: goal, saver_type: segment }); },
    detailsCaptured: function(p) { safePush('sl_details_captured', sanitise(p)); },
    projectionViewed: function(p) { safePush('sl_projection_viewed', p); },
    planGenerated: function(p) { safePush('sl_plan_generated', p); },
    paymentSimulated: function(status, p) { safePush('sl_payment_simulated', Object.assign({ payment_status: status }, p || {})); },
    demoSubmit: function(p) { safePush('sl_demo_submit', p); },
    staffAssistStarted: function(p) { safePush('sl_staff_assist_started', p); },
    dropoffDetected: function(step, p) { safePush('sl_dropoff', Object.assign({ dropoff_step: step }, p || {})); }
  };

}(window));
