"""Shopping cart views."""
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from ...models import Product
from ...services.cart_service import CartService
from django.http import JsonResponse


class CartView(TemplateView):
    """Display shopping cart with items and total."""
    template_name = 'shop/cart.html'
    
    def get_context_data(self, **kwargs):
        """Add cart data to context."""
        context = super().get_context_data(**kwargs)
        cart_service = CartService(self.request)
        
        context['cart_items'] = cart_service.get_cart_items()
        context['cart_total'] = cart_service.get_total()
        context['item_count'] = cart_service.get_item_count()
        
        return context


def add_to_cart(request, product_id):
    """Add product to cart via POST request."""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_service = CartService(request)
        
        if cart_service.add_to_cart(product_id, quantity):
            messages.success(request, 'Product added to cart!')
        else:
            messages.error(request, 'Product not available!')
        
        return redirect('shop:product-detail', slug=product.slug)
    
    return redirect('shop:product-list')


def remove_from_cart(request, product_id):
    """Remove product from cart."""
    cart_service = CartService(request)
    
    if cart_service.remove_from_cart(product_id):
        messages.success(request, 'Product removed from cart!')
    
    return redirect('shop:cart')


def update_cart(request, product_id):
    """Update product quantity in cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_service = CartService(request)
        
        if cart_service.update_quantity(product_id, quantity):
            messages.success(request, 'Cart updated!')
        else:
            messages.error(request, 'Error updating cart!')
    
    return redirect('shop:cart')

def cart_count_api(request):
    """Return cart item count as JSON."""
    cart_service = CartService(request)
    return JsonResponse({
        'count': cart_service.get_item_count()
    })
