from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:order_id>/', views.stripe_checkout_view, name='stripe_checkout'),
    path('sandbox-confirm/<int:order_id>/', views.sandbox_confirm_payment, name='sandbox_confirm'),
    path('success/<int:order_id>/', views.payment_success_view, name='success'),
    path('cancel/<int:order_id>/', views.payment_cancel_view, name='cancel'),
    path('webhook/', views.stripe_webhook_view, name='webhook'),
]
