import hmac
import hashlib
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .models import Payment


@csrf_exempt
def stripe_webhook(request):
    # Simple webhook verification using a shared secret header (X-Stripe-Signature simulation)
    sig = request.headers.get('X-Stripe-Signature')
    payload = request.body
    secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    if secret:
        if not sig:
            return HttpResponseBadRequest('Missing signature')
        expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, sig):
            return HttpResponseBadRequest('Invalid signature')

    try:
        data = json.loads(payload.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid payload')

    # expect payload like: {'type': 'payment_intent.succeeded', 'data': {'object': {'metadata': {'order_id': 1}, 'id': 'pi_123', 'amount': '100.00'}}}
    event_type = data.get('type')
    obj = data.get('data', {}).get('object', {})
    metadata = obj.get('metadata', {})
    order_id = metadata.get('order_id')

    if event_type == 'payment_intent.succeeded' and order_id:
        try:
            order = Order.objects.get(pk=int(order_id))
        except Order.DoesNotExist:
            return HttpResponseBadRequest('Order not found')

        amt = obj.get('amount')
        provider_id = obj.get('id')
        Payment.objects.create(order=order, provider='stripe', provider_payment_id=provider_id, amount=amt, status='succeeded')
        order.status = 'paid'
        order.save()
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'ignored'})
