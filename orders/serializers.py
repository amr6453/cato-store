from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_amount', 'created_at', 'items')
        read_only_fields = ('user', 'status', 'total_amount', 'created_at')



class OrderCreateItem(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderCreateSerializer(serializers.Serializer):
    items = OrderCreateItem(many=True)

