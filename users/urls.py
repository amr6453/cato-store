from django.urls import path
from .views import register, login, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
from django.urls import path
from . import views
from users.api import UserProfileViewSet

app_name = 'users'

profile_view = UserProfileViewSet.as_view({'get': 'me', 'patch': 'partial_update', 'put': 'partial_update'})

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # profile endpoints
    path('profile/me/', profile_view, name='profile_me'),
]
