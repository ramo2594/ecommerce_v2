"""
Admin module initialization.

Imports all admin classes for automatic registration.
"""

from .category_admin import CategoryAdmin
from .product_admin import ProductAdmin
from .customer_admin import CustomerAdmin
from .order_admin import OrderAdmin, OrderItemInline

__all__ = [
    'CategoryAdmin',
    'ProductAdmin',
    'CustomerAdmin',
    'OrderAdmin',
    'OrderItemInline',
]
