import graphene
from graphene_django import DjangoObjectType
from .models import Order, OrderItem
from products.models import Product
from django.db import transaction


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_amount', 'created_at', 'items')


class OrderItemInput(graphene.InputObjectType):
    product_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)


class GuestCreateOrder(graphene.Mutation):
    class Arguments:
        items = graphene.List(OrderItemInput, required=True)

    ok = graphene.Boolean()
    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(self, info, items):
        # Create a guest order (no user). Basic stock checks
        with transaction.atomic():
            order = Order.objects.create(user=None, status='pending', total_amount=0)
            total = 0
            for it in items:
                try:
                    product = Product.objects.select_for_update().get(pk=it.product_id)
                except Product.DoesNotExist:
                    return GuestCreateOrder(ok=False, message=f'Product {it.product_id} not found')
                if product.stock_quantity < it.quantity:
                    return GuestCreateOrder(ok=False, message=f'Not enough stock for {product.name}')
                OrderItem.objects.create(order=order, product=product, quantity=it.quantity, price=product.price)
                product.stock_quantity -= it.quantity
                product.save()
                total += product.price * it.quantity

            order.total_amount = total
            order.save()
            return GuestCreateOrder(ok=True, order=order)


class Mutation(graphene.ObjectType):
    guest_create_order = GuestCreateOrder.Field()
    create_order = graphene.Field(lambda: CreateOrder)


class CreateOrder(graphene.Mutation):
    class Arguments:
        items = graphene.List(OrderItemInput, required=True)

    ok = graphene.Boolean()
    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(self, info, items):
        user = info.context.user if hasattr(info.context, 'user') else None
        if user is None or not user.is_authenticated:
            return CreateOrder(ok=False, message='Authentication required')

        with transaction.atomic():
            order = Order.objects.create(user=user, status='pending', total_amount=0)
            total = 0
            for it in items:
                try:
                    product = Product.objects.select_for_update().get(pk=it.product_id)
                except Product.DoesNotExist:
                    return CreateOrder(ok=False, message=f'Product {it.product_id} not found')
                if product.stock_quantity < it.quantity:
                    return CreateOrder(ok=False, message=f'Not enough stock for {product.name}')
                OrderItem.objects.create(order=order, product=product, quantity=it.quantity, price=product.price)
                product.stock_quantity -= it.quantity
                product.save()
                total += product.price * it.quantity

            order.total_amount = total
            order.save()
            return CreateOrder(ok=True, order=order)


class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int())

    def resolve_orders(self, info):
        return Order.objects.all()

    def resolve_order(self, info, id=None):
        if id is None:
            return None
        return Order.objects.filter(pk=id).first()
