"""
Shop models package initialization.

Enterprise models for e-commerce:
- Category: Product categories
"""
from .category import Category
from .product import Product

__all__ = [
    'Category',
    'Product',
]