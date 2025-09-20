from django.urls import path
from . import views

urlpatterns = [
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
