from django.test import TestCase
from .models import Product


class ProductModelTest(TestCase):
    def test_create_product(self):
        p = Product.objects.create(name='Test', price='9.99')
        self.assertEqual(str(p), 'Test')
        self.assertTrue(p.slug)
