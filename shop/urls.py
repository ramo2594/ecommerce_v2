"""
Shop app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Product URLs
    path('products/', views.product_list, name='product-list'),
    path('products/<slug:slug>/', views.product_detail, name='product-detail'),
    
    # Category URLs
    path('categories/', views.category_list, name='category-list'),
    path('categories/<slug:slug>/', views.category_detail, name='category-detail'),
]
