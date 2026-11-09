"""
URL Configuration for GrX Parfums.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Custom Handcrafted Administration Panel (A9)
    path('admin-dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # Standard Django admin (internal fallback)
    path('django-admin/', admin.site.urls),

    # Core Application Routes
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),

    # Catalog & Home (A1, A2)
    path('', include('apps.catalog.urls', namespace='catalog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
