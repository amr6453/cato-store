from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # users see only their orders unless staff
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        """Convert session cart to an Order. Expects session['cart'] = {product_id: quantity} """
        cart = request.session.get('cart', {})
        if not cart:
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        with transaction.atomic():
            order = Order.objects.create(user=user, status='pending', total_amount=0)
            total = 0
            for pid_str, qty in cart.items():
                try:
                    pid = int(pid_str)
                    product = Product.objects.select_for_update().get(pk=pid)
                except (ValueError, Product.DoesNotExist):
                    transaction.set_rollback(True)
                    return Response({'detail': f'Invalid product id {pid_str}'}, status=status.HTTP_400_BAD_REQUEST)

                if product.stock_quantity < qty:
                    transaction.set_rollback(True)
                    return Response({'detail': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)

                item = OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
                product.stock_quantity -= qty
                product.save()
                total += product.price * qty

            order.total_amount = total
            order.save()
            # clear cart
            request.session['cart'] = {}
            request.session.modified = True

            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def create_from_payload(self, request):
        """Create order from JSON payload: {'items': [{'product_id': 1, 'quantity': 2}, ...]}"""
        from .serializers import OrderCreateSerializer

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = serializer.validated_data['items']

        user = request.user
        if not items:
            return Response({'detail': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user=user, status='pending', total_amount=0)
            total = 0
            for it in items:
                try:
                    product = Product.objects.select_for_update().get(pk=it['product_id'])
                except Product.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response({'detail': f"Product {it['product_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)

                qty = it['quantity']
                if product.stock_quantity < qty:
                    transaction.set_rollback(True)
                    return Response({'detail': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)

                item = OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
                product.stock_quantity -= qty
                product.save()
                total += product.price * qty

            order.total_amount = total
            order.save()
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
