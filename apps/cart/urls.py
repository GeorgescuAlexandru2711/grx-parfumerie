from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='detail'),
    path('add/<int:variant_id>/', views.cart_add_view, name='add'),
    path('update/<int:variant_id>/', views.cart_update_view, name='update'),
    path('remove/<int:variant_id>/', views.cart_remove_view, name='remove'),
    path('samples/', views.cart_samples_view, name='samples'),
    path('coupon/apply/', views.apply_coupon_view, name='apply_coupon'),
    path('coupon/remove/', views.remove_coupon_view, name='remove_coupon'),
]
