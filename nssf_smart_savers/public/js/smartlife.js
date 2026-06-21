/**
 * SmartLife Flexi - Main JS
 * Stepper, validation, projection, payment simulation
 */
(function (window) {
  'use strict';

  // PII patterns for client-side detection
  var NIN_RE = /^[A-Z]{2}\d{7}[A-Z]{2}$/i;
  var PHONE_RE = /^(\+?256|0)[7][0-9]{8}$/;

  function looksLikeNIN(val) {
    return NIN_RE.test((val || '').trim());
  }

  function looksLikePhone(val) {
    return PHONE_RE.test((val || '').replace(/[\s\-()]/g, ''));
  }

  function hasPII(val) {
    return looksLikeNIN(val) || looksLikePhone(val);
  }

  // Debounce helper
  function debounce(fn, delay) {
    var timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(fn, delay);
    };
  }

  // Format UGX
  function formatUGX(amount) {
    return 'UGX ' + Math.round(amount || 0).toLocaleString();
  }

  // SmartLife namespace
  window.SmartLife = window.SmartLife || {};

  SmartLife.hasPII = hasPII;
  SmartLife.formatUGX = formatUGX;

  // Validate any text input for PII
  SmartLife.validateInput = function (el) {
    var val = el.value || '';
    if (hasPII(val)) {
      el.value = '';
      var warning = el.closest('.sl-field') && el.closest('.sl-field').querySelector('.sl-pii-warning');
      if (warning) warning.style.display = 'block';
      return false;
    }
    return true;
  };

  // Generic stepper (used in self-serve)
  SmartLife.Stepper = function (opts) {
    this.currentStep = opts.startStep || 1;
    this.totalSteps = opts.totalSteps || 5;
    this.stepPrefix = opts.stepPrefix || 'sl-step-';
    this.indicatorPrefix = opts.indicatorPrefix || '[data-step="';
    this.state = opts.state || {};
    this.onStepChange = opts.onStepChange || function () {};
  };

  SmartLife.Stepper.prototype.goTo = function (n) {
    if (n < 1 || n > this.totalSteps) return;
    var prev = this.currentStep;
    var stepEl = document.getElementById(this.stepPrefix + prev);
    if (stepEl) stepEl.classList.remove('active');
    var indEl = document.querySelector('[data-step="' + prev + '"]');
    if (indEl) indEl.classList.remove('active');

    this.currentStep = n;
    var nextEl = document.getElementById(this.stepPrefix + n);
    if (nextEl) nextEl.classList.add('active');
    var nextIndEl = document.querySelector('[data-step="' + n + '"]');
    if (nextIndEl) nextIndEl.classList.add('active');

    window.scrollTo(0, 0);
    this.onStepChange(n, prev);
  };

  SmartLife.Stepper.prototype.next = function () { this.goTo(this.currentStep + 1); };
  SmartLife.Stepper.prototype.prev = function () { this.goTo(this.currentStep - 1); };

  // Projection fetch
  SmartLife.fetchProjection = function (params, callback) {
    var qs = new URLSearchParams(params).toString();
    fetch('/api/method/nssf_smart_savers.api.get_projection?' + qs)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        callback(null, data.message || data);
      })
      .catch(function (e) {
        callback(e, null);
      });
  };

  // Plan fetch
  SmartLife.fetchPlan = function (params, callback) {
    var qs = new URLSearchParams(params).toString();
    fetch('/api/method/nssf_smart_savers.api.get_personalised_plan_api?' + qs)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        callback(null, data.message || data);
      })
      .catch(function (e) {
        callback(e, null);
      });
  };

  // Submit lead
  SmartLife.submitLead = function (params, callback) {
    var qs = new URLSearchParams(params).toString();
    fetch('/api/method/nssf_smart_savers.api.submit_demo_lead?' + qs)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        callback(null, data.message || data);
      })
      .catch(function (e) {
        callback(e, null);
      });
  };

  // Detect dirty form state for dropoff
  var _formDirty = false;
  document.addEventListener('input', function () { _formDirty = true; });
  window.addEventListener('beforeunload', function () {
    if (_formDirty && window.SmartLifeAnalytics) {
      SmartLifeAnalytics.dropoffDetected('page_exit', {
        journey_type: 'self_serve'
      });
    }
  });

  // Init on page load
  document.addEventListener('DOMContentLoaded', function () {
    // Auto-attach PII check to all text inputs on smartlife pages
    document.querySelectorAll('.smartlife-form input[type="text"]').forEach(function (el) {
      el.addEventListener('blur', function () {
        SmartLife.validateInput(el);
      });
    });
  });

}(window));
