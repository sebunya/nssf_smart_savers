/**
 * SmartLife Flexi - Analytics Helper
 * Sanitises params before pushing to GTM dataLayer
 * GTM Container: GTM-PZRV3MQL
 * Never sends PII
 */
(function (window) {
  'use strict';

  var ALLOWED_PARAMS = [
    'journey_type', 'segment', 'goal_category', 'frequency', 'period_band',
    'target_band', 'source_category', 'industry_category', 'country_band',
    'step_name', 'staff_assisted', 'payment_status', 'completion_status',
    'dropoff_step', 'lead_stage'
  ];

  window.SmartLifeAnalytics = {
    ALLOWED_PARAMS: ALLOWED_PARAMS,

    sanitise: function (params) {
      var safe = {};
      if (!params || typeof params !== 'object') return safe;
      ALLOWED_PARAMS.forEach(function (k) {
        if (params[k] !== undefined && params[k] !== null) {
          safe[k] = String(params[k]).slice(0, 100);
        }
      });
      return safe;
    },

    push: function (eventName, params) {
      window.dataLayer = window.dataLayer || [];
      var safe = this.sanitise(params || {});
      window.dataLayer.push(Object.assign({ event: String(eventName).slice(0, 100) }, safe));
    },

    demoView: function (params) {
      this.push('sl_demo_view', params);
    },

    segmentSelected: function (segment) {
      this.push('sl_segment_selected', { segment: segment });
    },

    goalSelected: function (goal, segment) {
      this.push('sl_goal_selected', { goal_category: goal, segment: segment });
    },

    projectionViewed: function (params) {
      this.push('sl_projection_viewed', params);
    },

    planGenerated: function (params) {
      this.push('sl_plan_generated', params);
    },

    staffAssistStarted: function (params) {
      this.push('sl_staff_assist_started', params);
    },

    demoSubmit: function (params) {
      this.push('sl_demo_submit', params);
    },

    paymentSimulated: function (status, params) {
      this.push('sl_payment_simulated', Object.assign({ payment_status: status }, params || {}));
    },

    supportRequested: function (params) {
      this.push('sl_support_requested', params);
    },

    dropoffDetected: function (step, params) {
      this.push('sl_dropoff_detected', Object.assign({ dropoff_step: step }, params || {}));
      // Also fire API log for backend tracking
      try {
        var p = Object.assign({ dropoff_step: step }, params || {});
        navigator.sendBeacon && navigator.sendBeacon(
          '/api/method/nssf_smart_savers.api.log_dropoff',
          JSON.stringify({ step_name: step, segment: p.segment || '', goal: p.goal || '', journey_type: p.journey_type || 'self_serve' })
        );
      } catch (e) {}
    }
  };

}(window));
