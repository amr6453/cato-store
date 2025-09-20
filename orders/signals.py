from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Order
from django.conf import settings


@receiver(post_save, sender=Order)
def order_post_save(sender, instance: Order, created, **kwargs):
    if created:
        # send order created email
        subject = f"Order #{instance.pk} received"
        body = render_to_string('emails/order_created.txt', {'order': instance})
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=True)
    else:
        # if status changed to paid, send payment confirmation
        if instance.status == 'paid':
            subject = f"Order #{instance.pk} payment confirmed"
            body = render_to_string('emails/order_paid.txt', {'order': instance})
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=True)
