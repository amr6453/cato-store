from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Product
from django.contrib.auth import get_user_model


User = get_user_model()


class OrdersAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='orderuser', password='pass')
        self.prod = Product.objects.create(name='P1', slug='p1', description='x', price=5.0, stock_quantity=10, is_active=True)

    def test_create_order_from_cart(self):
        self.client.force_authenticate(self.user)
        session = self.client.session
        session['cart'] = {str(self.prod.pk): 2}
        session.save()

        resp = self.client.post('/api/orders/create_from_cart/')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        # total_amount may be serialized as a string/Decimal; compare numerically
        self.assertAlmostEqual(float(data['total_amount']), 10.0)

    def test_create_order_insufficient_stock(self):
        self.client.force_authenticate(self.user)
        session = self.client.session
        session['cart'] = {str(self.prod.pk): 20}
        session.save()

        resp = self.client.post('/api/orders/create_from_cart/')
        self.assertEqual(resp.status_code, 400)

    def test_create_order_from_payload(self):
        self.client.force_authenticate(self.user)
        payload = {'items': [{'product_id': self.prod.pk, 'quantity': 3}]}
        resp = self.client.post('/api/orders/create_from_payload/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertAlmostEqual(float(data['total_amount']), 15.0)

    def test_create_order_from_payload_insufficient(self):
        self.client.force_authenticate(self.user)
        payload = {'items': [{'product_id': self.prod.pk, 'quantity': 999}]}
        resp = self.client.post('/api/orders/create_from_payload/', payload, format='json')
        self.assertEqual(resp.status_code, 400)
