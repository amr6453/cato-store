"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.api import ProductViewSet
from orders.api import OrderViewSet
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .auth import JWTGraphQLView
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve as static_serve

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    # `store` app default mounting moved below depending on whether a
    # built frontend exists (we want the SPA at `/` when available).
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    # API
    path('api/', include(router.urls)),
    path('api/auth/', include('users.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/schema/', get_schema_view(title='Cato Store API'), name='openapi-schema'),
    path('api/docs/', TemplateView.as_view(template_name='docs.html', extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),
    path('graphql/', csrf_exempt(JWTGraphQLView.as_view(graphiql=True))),
    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# If the frontend has been built, serve the index.html for the root and any
# unmatched path so client-side routing works. This should come last so API
# and admin paths take precedence.
dist_path = (settings.BASE_DIR / 'frontend' / 'dist')
if dist_path.exists():
    dist_dir = dist_path
    # serve built assets (vite outputs) directly at /assets/* so index.html can
    # reference them using absolute paths produced by Vite (e.g. /assets/...)
    urlpatterns += [
        path('assets/<path:path>', static_serve, {'document_root': str(dist_dir / 'assets')}),
        path('favicon.ico', static_serve, {'document_root': str(dist_dir), 'path': 'favicon.ico'}),
        # If the frontend is present, mount the legacy Django pages under
        # /legacy/ and let the SPA handle the root.
        path('legacy/', include('store.urls')),
        path('', TemplateView.as_view(template_name='index.html'), name='frontend-index'),
        path('<path:unused>/', TemplateView.as_view(template_name='index.html')),
    ]
else:
    # No built frontend — mount the store app at root as before
    urlpatterns = [path('', include('store.urls'))] + urlpatterns
