from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Seed sample products for development'

    def handle(self, *args, **options):
        items = [
            {'name': 'Blue T-Shirt', 'slug': 'blue-t-shirt', 'description': 'A comfortable blue t-shirt made from organic cotton.', 'price': '19.99', 'stock_quantity': 50},
            {'name': 'Red Mug', 'slug': 'red-mug', 'description': 'Ceramic mug with a glossy red finish.', 'price': '9.50', 'stock_quantity': 100},
        ]
        for it in items:
            p, created = Product.objects.get_or_create(slug=it['slug'], defaults=it)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {p.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product exists: {p.name}"))
