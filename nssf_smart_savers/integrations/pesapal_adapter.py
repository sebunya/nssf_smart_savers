"""
SmartLife Flexi - Pesapal Payment Adapter
Demo/Sandbox architecture only. No real payments in Phase 1.
To activate: set site_config pesapal_consumer_key, pesapal_consumer_secret, pesapal_mode.
"""
import frappe

DEMO_MODE = 'demo'
SANDBOX_MODE = 'sandbox'
LIVE_MODE = 'live'


def get_pesapal_config():
    """Read Pesapal config from site_config. Never hard-coded."""
    return {
        'mode': frappe.conf.get('pesapal_mode', DEMO_MODE),
        'consumer_key': frappe.conf.get('pesapal_consumer_key', ''),
        'consumer_secret': frappe.conf.get('pesapal_consumer_secret', ''),
        'callback_url': frappe.conf.get('pesapal_callback_url', ''),
        'ipn_url': frappe.conf.get('pesapal_ipn_url', ''),
    }


def is_demo_mode():
    return get_pesapal_config()['mode'] == DEMO_MODE


def create_demo_order(amount, currency='UGX', description='SmartLife Flexi Demo Contribution',
                       reference=None):
    """Create a demo order record. No real API call in demo mode."""
    import uuid
    ref = reference or ('SL-DEMO-' + str(uuid.uuid4())[:8].upper())
    return {
        'order_tracking_id': ref,
        'status': 'PENDING',
        'amount': amount,
        'currency': currency,
        'description': description,
        'demo': True,
        'redirect_url': '/smartlife-checkout-demo?status=demo_pending&ref=' + ref,
    }


def build_checkout_payload(amount, currency='UGX', description='SmartLife Flexi Demo',
                            reference=None, callback_url=None):
    """Build Pesapal IPN/checkout payload structure."""
    config = get_pesapal_config()
    if is_demo_mode():
        return create_demo_order(amount, currency, description, reference)

    return {
        'Amount': amount,
        'Description': description,
        'Type': 'MERCHANT',
        'Reference': reference,
        'CallBackURL': callback_url or config['callback_url'],
        'currency': currency,
        'Mode': config['mode'],
    }


def verify_payment_callback(params):
    """Verify a Pesapal payment callback. Demo mode always returns simulated success."""
    if is_demo_mode():
        return {
            'status': 'COMPLETED',
            'reference': params.get('pesapal_merchant_reference', ''),
            'transaction_id': params.get('pesapal_transaction_tracking_id', ''),
            'demo': True,
        }
    # Live: implement actual Pesapal QueryPaymentStatus API call
    raise NotImplementedError('Live Pesapal verification requires credentials in site_config.')


def handle_ipn(params):
    """Handle Pesapal IPN notification. Demo mode logs only."""
    if is_demo_mode():
        frappe.log_error('Pesapal IPN (demo): ' + str(params), 'SmartLife Pesapal Demo IPN')
        return {'status': 'ok', 'demo': True}
    raise NotImplementedError('Live IPN handling requires Pesapal credentials.')
