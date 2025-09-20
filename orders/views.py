from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Order, OrderItem


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for slug, qty in cart.items():
        try:
            p = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            continue
        items.append({'product': p, 'quantity': qty, 'subtotal': p.price * qty})
        total += p.price * qty
    return render(request, 'orders/cart.html', {'items': items, 'total': total})


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('products:product_list')

    # naive checkout: create order and clear cart
    order = Order.objects.create(total_amount=0)
    total = 0
    for slug, qty in cart.items():
        p = get_object_or_404(Product, slug=slug)
        oi = OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
        total += p.price * qty
    order.total_amount = total
    order.save()
    request.session['cart'] = {}
    return render(request, 'orders/checkout_complete.html', {'order': order})


def add_to_cart(request, slug):
    if request.method != 'POST':
        return redirect('products:product_detail', slug=slug)
    qty = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    cart[slug] = cart.get(slug, 0) + max(1, qty)
    request.session['cart'] = cart
    return redirect('orders:view_cart')
