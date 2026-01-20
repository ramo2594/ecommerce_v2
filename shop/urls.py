"""Shop app URL configuration."""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views.cart.views import CartView, add_to_cart, remove_from_cart, update_cart, cart_count_api 
from .views import (
    ProductListView,
    ProductDetailView,
    CartView,
    add_to_cart,
    remove_from_cart,
    update_cart,
    cart_count_api,
    CheckoutView,
    OrderConfirmationView,
    RegisterView,
    LoginView,
    logout_view,
    UserOrdersListView,
    OrderDetailView,
)
from django.views.generic import TemplateView

app_name = 'shop'

# Temporary placeholder view
class ComingSoonView(TemplateView):
    template_name = 'shop/coming_soon.html'

urlpatterns = [
    # Products
    path('', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update-cart'),
    path('api/cart/count/', cart_count_api, name='cart-api-count'),
    
    # Checkout & Orders
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/<str:order_number>/', OrderConfirmationView.as_view(), name='order-confirmation'),
    path('orders/', UserOrdersListView.as_view(), name='user-orders'),
    path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),

    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
