"""
Shop views package initialization.
"""
from .main import (
    ProductListView,
    ProductDetailView,
    CartView,
    add_to_cart,
    remove_from_cart,
    update_cart,
)
from .checkout.views import CheckoutView, OrderConfirmationView

__all__ = [
    'ProductListView',
    'ProductDetailView',
    'CartView',
    'add_to_cart',
    'remove_from_cart',
    'update_cart',
    'CheckoutView',
    'OrderConfirmationView',
]