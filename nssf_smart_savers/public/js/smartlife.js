/**
 * SmartLife Flexi - Global JS Utilities
 * Page-specific logic lives in each page's <script> block.
 * This file provides shared utilities only.
 */
(function (window) {
  'use strict';

  var NIN_RE = /^[A-Z]{2}\d{7}[A-Z]{2}$/i;
  var PHONE_RE = /^(\+?256|0)[7][0-9]{8}$/;

  window.SmartLife = window.SmartLife || {};

  SmartLife.hasPII = function(val) {
    val = String(val || '').trim();
    return NIN_RE.test(val) || PHONE_RE.test(val.replace(/[\s\-()]/g, ''));
  };

  SmartLife.formatUGX = function(amount) {
    return 'UGX ' + Math.round(amount || 0).toLocaleString();
  };

  SmartLife.periodBand = function(years) {
    years = parseInt(years) || 0;
    if (years <= 1) return '1y';
    if (years <= 3) return '1-3y';
    if (years <= 5) return '3-5y';
    if (years <= 10) return '5-10y';
    return '10y+';
  };

  SmartLife.safeGet = function(id) {
    return document.getElementById(id);
  };

  // Form-dirty tracking for dropoff detection
  var _dirty = false;
  document.addEventListener('input', function() { _dirty = true; });
  SmartLife.isFormDirty = function() { return _dirty; };

  // PII validation on text inputs with class sl-safe-input
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sl-safe-input').forEach(function(el) {
      el.addEventListener('blur', function() {
        if (SmartLife.hasPII(this.value)) {
          this.value = '';
          var alert = document.getElementById('sl-pii-alert');
          if (alert) alert.style.display = 'block';
        }
      });
    });
  });

}(window));
