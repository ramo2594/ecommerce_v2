"""Shop app URL configuration."""
from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ProductListView,
    ProductDetailView,
    CartView,
    add_to_cart,
    remove_from_cart,
    update_cart,
    CheckoutView,
    OrderConfirmationView,
)

app_name = 'shop'

# Temporary placeholder view
class ComingSoonView(TemplateView):
    template_name = 'shop/coming_soon.html'

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update-cart'),
    
        # Checkout & Orders
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/<str:order_number>/', OrderConfirmationView.as_view(), name='order-confirmation'),
    path('orders/', ComingSoonView.as_view(), name='order-list'),
]
