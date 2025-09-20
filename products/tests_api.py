from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Product.objects.create(name='Test Product', slug='test-product', description='x', price=10.0, stock_quantity=5, is_active=True)

    def test_list_products(self):
        resp = self.client.get('/api/products/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # DRF pagination returns an object with 'results'
        if isinstance(data, dict) and 'results' in data:
            items = data['results']
        else:
            items = data

        self.assertIsInstance(items, list)
        self.assertGreaterEqual(len(items), 1)
