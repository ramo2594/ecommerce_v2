"""
Cart business logic service.
Handles session-based shopping cart operations.
"""
from decimal import Decimal
from django.contrib.auth.models import User
from ..models import Product


class CartService:
    """Service for managing shopping cart operations."""
    
    CART_SESSION_KEY = 'cart'
    
    def __init__(self, request):
        """Initialize CartService with request object."""
        self.request = request
        self.session = request.session
        self.cart = self.session.get(self.CART_SESSION_KEY, {})
    
    def add_to_cart(self, product_id: int, quantity: int = 1) -> bool:
        """
        Add product to cart.
        
        Args:
            product_id: Product ID to add
            quantity: Quantity (default 1)
            
        Returns:
            bool: True if successful, False if product unavailable
        """
        try:
            product = Product.objects.get(id=product_id)
            
            if not product.is_available or product.stock < quantity:
                return False
            
            product_id_str = str(product_id)
            
            if product_id_str in self.cart:
                self.cart[product_id_str]['quantity'] += quantity
            else:
                self.cart[product_id_str] = {
                    'quantity': quantity,
                    'price': str(product.price),
                }
            
            self._save_cart()
            return True
            
        except Product.DoesNotExist:
            return False
    
    def remove_from_cart(self, product_id: int) -> bool:
        """Remove product from cart."""
        product_id_str = str(product_id)
        
        if product_id_str in self.cart:
            del self.cart[product_id_str]
            self._save_cart()
            return True
        
        return False
    
    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """Update product quantity in cart."""
        product_id_str = str(product_id)
        
        if product_id_str not in self.cart:
            return False
        
        if quantity <= 0:
            return self.remove_from_cart(product_id)
        
        try:
            product = Product.objects.get(id=product_id)
            
            if product.stock < quantity:
                return False
            
            self.cart[product_id_str]['quantity'] = quantity
            self._save_cart()
            return True
            
        except Product.DoesNotExist:
            return False
    
    def get_cart_items(self):
        """Get cart items with full product data."""
        items = []
        
        for product_id_str, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                items.append({
                    'product': product,
                    'quantity': item_data['quantity'],
                    'price': Decimal(item_data['price']),
                    'subtotal': Decimal(item_data['price']) * item_data['quantity'],
                })
            except Product.DoesNotExist:
                # Rimuovi prodotti eliminati
                del self.cart[product_id_str]
        
        self._save_cart()
        return items
    
    def get_total(self) -> Decimal:
        """Calculate cart total."""
        total = Decimal('0.00')
        
        for item in self.get_cart_items():
            total += item['subtotal']
        
        return total
    
    def get_item_count(self) -> int:
        """Get total number of items in cart."""
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear_cart(self):
        """Clear entire cart."""
        self.cart = {}
        self._save_cart()
    
    def _save_cart(self):
        """Save cart to session."""
        self.session[self.CART_SESSION_KEY] = self.cart
        self.session.modified = True
