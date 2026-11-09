from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='list'),
    path('search/', views.search_view, name='search'),
    path('category/<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    path('family/<slug:family_slug>/', views.fragrance_family_detail_view, name='family_detail'),
    path('fragrance/<slug:slug>/', views.product_detail_view, name='product_detail'),
]
