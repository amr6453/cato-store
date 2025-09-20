from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()


class OrderEmailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='emailuser', email='u@example.com', password='pass')

    def test_order_created_sends_email(self):
        mail.outbox = []
        Order.objects.create(user=self.user, status='pending', total_amount=12.0)
        # one email should be queued
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_order_paid_sends_email(self):
        mail.outbox = []
        order = Order.objects.create(user=self.user, status='pending', total_amount=12.0)
        order.status = 'paid'
        order.save()
        self.assertGreaterEqual(len(mail.outbox), 1)
