from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_overview, name='overview'),

    # Product Catalog Management
    path('products/', views.dashboard_products, name='products'),
    path('products/create/', views.dashboard_product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.dashboard_product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.dashboard_product_delete, name='product_delete'),
    path('products/<int:product_id>/variants/add/', views.dashboard_variant_add, name='variant_add'),
    path('variants/<int:variant_id>/delete/', views.dashboard_variant_delete, name='variant_delete'),

    # Inventory & Stock
    path('inventory/', views.dashboard_inventory, name='inventory'),
    path('inventory/restock/', views.dashboard_inventory_restock, name='inventory_restock'),

    # Order Management
    path('orders/', views.dashboard_orders, name='orders'),
    path('orders/<int:pk>/', views.dashboard_order_detail, name='order_detail'),
    path('orders/<int:pk>/status/', views.dashboard_order_status_update, name='order_status_update'),

    # Customers
    path('customers/', views.dashboard_customers, name='customers'),
]
