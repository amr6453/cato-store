from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product


class ProductAPIMoreTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        for i in range(15):
            Product.objects.create(name=f'P{i}', slug=f'p{i}', description='desc', price=1.0 + i, stock_quantity=10, is_active=True)

    def test_pagination_default(self):
        resp = self.client.get('/api/products/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 12)

    def test_search(self):
        resp = self.client.get('/api/products/?search=P1')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(len(data['results']), 1)

    def test_ordering(self):
        resp = self.client.get('/api/products/?ordering=price')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        prices = [float(item['price']) for item in data['results']]
        self.assertEqual(prices, sorted(prices))
