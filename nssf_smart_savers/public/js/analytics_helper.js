/**
 * SmartLife Flexi - Analytics Helper
 * Wraps GTM dataLayer pushes. Safe for demo - no PII allowed.
 */
(function(window) {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  function safePush(eventName, params) {
    try {
      var payload = { event: eventName };
      if (params && typeof params === 'object') {
        Object.keys(params).forEach(function(k) {
          payload[k] = String(params[k] || '').slice(0, 100);
        });
      }
      payload.demo_environment = 'true';
      window.dataLayer.push(payload);
    } catch(e) {
      // Analytics must never break the page
    }
  }

  window.SmartLifeAnalytics = {
    push: function(eventName, params) { safePush(eventName, params); },
    demoView: function(p) { safePush('sl_demo_view', p); },
    segmentSelected: function(segment) { safePush('sl_segment_selected', { segment: segment }); },
    goalSelected: function(goal, segment) { safePush('sl_goal_selected', { goal_category: goal, segment: segment }); },
    projectionViewed: function(p) { safePush('sl_projection_viewed', p); },
    planGenerated: function(p) { safePush('sl_plan_generated', p); },
    paymentSimulated: function(status, p) { safePush('sl_payment_simulated', Object.assign({ payment_status: status }, p || {})); },
    demoSubmit: function(p) { safePush('sl_demo_submit', p); },
    staffAssistStarted: function(p) { safePush('sl_staff_assist_started', p); },
    dropoffDetected: function(step, p) { safePush('sl_dropoff', Object.assign({ dropoff_step: step }, p || {})); }
  };

}(window));
