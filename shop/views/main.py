"""
Main shop views: Product listing and detail.
"""
from django.views.generic import ListView, DetailView
from ..models import Product, Category
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from ..services.cart_service import CartService


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

class CartView(TemplateView):
    """Display shopping cart."""
    template_name = 'shop/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_service = CartService(self.request)
        
        context['cart_items'] = cart_service.get_cart_items()
        context['cart_total'] = cart_service.get_total()
        context['item_count'] = cart_service.get_item_count()
        
        return context


def add_to_cart(request, product_id):
    """Add product to cart via POST."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_service = CartService(request)
        
        if cart_service.add_to_cart(product_id, quantity):
            messages.success(request, 'Prodotto aggiunto al carrello!')
        else:
            messages.error(request, 'Prodotto non disponibile!')
        
        return redirect('shop:product-detail', slug=request.POST.get('slug'))
    
    return redirect('shop:product-list')


def remove_from_cart(request, product_id):
    """Remove product from cart."""
    cart_service = CartService(request)
    
    if cart_service.remove_from_cart(product_id):
        messages.success(request, 'Prodotto rimosso dal carrello!')
    
    return redirect('shop:cart')


def update_cart(request, product_id):
    """Update product quantity in cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_service = CartService(request)
        
        if cart_service.update_quantity(product_id, quantity):
            messages.success(request, 'Carrello aggiornato!')
        else:
            messages.error(request, 'Errore aggiornamento carrello!')
    
    return redirect('shop:cart')