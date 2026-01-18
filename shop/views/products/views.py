"""Product views: listing and detail."""
from django.views.generic import ListView, DetailView
from django.db.models import Q
from ...models import Product, Category


class ProductListView(ListView):
    """Display all available products with filtering and search."""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Filter products by category and search query."""
        queryset = Product.objects.filter(is_available=True).select_related('category')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search by name or description
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add categories and search query to context."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProductDetailView(DetailView):
    """Display single product details with related products."""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    
    def get_queryset(self):
        """Filter only available products."""
        return Product.objects.filter(is_available=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        """Add related products to context."""
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get related products from same category (max 4, exclude current)
        context['related_products'] = (
            product.category.products.filter(is_available=True)
            .exclude(id=product.id)
            .select_related('category')[:4]
        )
        
        return context
