from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from products.models import Product
from orders.models import Order
from django.contrib.auth import get_user_model
import json, hmac, hashlib


User = get_user_model()


@override_settings(STRIPE_WEBHOOK_SECRET='wh_sec_test')
class PaymentsWebhookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='payuser', password='pass')
        self.prod = Product.objects.create(name='P1', slug='p1', description='x', price=5.0, stock_quantity=10, is_active=True)
        self.order = Order.objects.create(user=self.user, status='pending', total_amount=5.0)

    def _make_sig(self, payload_bytes):
        secret = 'wh_sec_test'
        return hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()

    def test_payment_intent_succeeded_webhook(self):
        payload = {
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'metadata': {'order_id': str(self.order.pk)},
                    'id': 'pi_test_1',
                    'amount': '5.00'
                }
            }
        }
        body = json.dumps(payload).encode('utf-8')
        sig = self._make_sig(body)
        resp = self.client.post('/api/payments/stripe/webhook/', data=body, content_type='application/json', **{'HTTP_X_STRIPE_SIGNATURE': sig})
        self.assertEqual(resp.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')
