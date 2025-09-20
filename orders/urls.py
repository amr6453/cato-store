from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
]