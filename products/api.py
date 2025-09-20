from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for products with search and ordering."""
    queryset = Product.objects.filter(is_active=True).order_by('-created_at').prefetch_related('images')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'slug']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    # Note: caching list responses caused stale results across tests/environments.
    # If you need response caching, use a cache layer external to the application
    # or add proper cache invalidation. For now, return the standard list.
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
