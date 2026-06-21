app_name = "nssf_smart_savers"
app_title = "Nssf Smart Savers"
app_publisher = " Ten-X Africa"
app_description = "Demo growth, onboarding and staff-assist system for SmartLife Flexi"
app_email = "robsebunya@gmail.com"
app_license = "mit"

# Website Route Rules
# -------------------
website_route_rules = [
    {"from_route": "/smartlife-flexi-demo", "to_route": "smartlife-flexi-demo"},
    {"from_route": "/smartlife-self-serve", "to_route": "smartlife-self-serve"},
    {"from_route": "/smartlife-staff-assist", "to_route": "smartlife-staff-assist"},
    {"from_route": "/smartlife-projection-demo", "to_route": "smartlife-projection-demo"},
    {"from_route": "/smartlife-checkout-demo", "to_route": "smartlife-checkout-demo"},
    {"from_route": "/smartlife-thank-you", "to_route": "smartlife-thank-you"},
    {"from_route": "/smartlife-support-demo", "to_route": "smartlife-support-demo"},
]

# Jinja
# ----------
jinja = {
    "methods": "nssf_smart_savers.utils.jinja_methods",
}

# Includes in <head>
# ------------------
app_include_css = ["/assets/nssf_smart_savers/css/smartlife.css"]
app_include_js = [
    "/assets/nssf_smart_savers/js/analytics_helper.js",
    "/assets/nssf_smart_savers/js/smartlife.js",
]

web_include_css = ["/assets/nssf_smart_savers/css/smartlife.css"]
web_include_js = [
    "/assets/nssf_smart_savers/js/analytics_helper.js",
    "/assets/nssf_smart_savers/js/smartlife.js",
]

# Generators
# ----------
website_generators = []
