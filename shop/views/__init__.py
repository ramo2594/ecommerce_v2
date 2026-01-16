"""Shop views package."""
from .products.views import ProductListView, ProductDetailView
from .cart.views import CartView, add_to_cart, remove_from_cart, update_cart, cart_count_api
from .checkout.views import CheckoutView, OrderConfirmationView
from .auth.views import RegisterView, LoginView, logout_view

__all__ = [
    'ProductListView',
    'ProductDetailView',
    'CartView',
    'add_to_cart',
    'remove_from_cart',
    'update_cart',
    'cart_count_api',
    'CheckoutView',
    'OrderConfirmationView',
    'RegisterView',
    'LoginView',
    'logout_view',
]
