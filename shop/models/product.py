"""
Product Model: Represents sellable items in the e-commerce platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from ..constants import (
    MIN_PRICE, MAX_PRICE,
    MIN_STOCK, MAX_STOCK,
    MAX_QUANTITY,
    PRODUCT_IMAGE_UPLOAD_PATH
)

class Product(models.Model):
    """
    E-commerce product model.
    
    Represents a sellable item with pricing, inventory, and categorization.
    
    Attributes:
        name (str): Unique product name/identifier
        slug (str): URL-friendly identifier (auto-generated from name)
        category (ForeignKey): Link to product category
        price (Decimal): Price in EUR with 2 decimal places
        description (str): Detailed product description
        image (ImageField): Optional product image
        is_available (bool): Whether product is available for purchase
        stock (int): Number of units in warehouse
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last modification timestamp
    """
    
    name = models.CharField(
        max_length=200,
        unique=False,
        db_index=True,
        verbose_name=_("Product Name"),
        help_text=_("Ex: iPhone 17 Pro, T-shirt Cotton White")
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name=_("Slug"),
        default='',
        help_text=_("URL-friendly identifier (auto-generated)")
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_("Category")
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_PRICE),
            MaxValueValidator(MAX_PRICE)
        ],
        verbose_name=_("Price")
    )

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Detailed product description for customers")
    )

    image = models.ImageField(
        upload_to=PRODUCT_IMAGE_UPLOAD_PATH,
        blank=True,
        null=True,
        verbose_name=_("Product Image"),
        help_text=_("Optional product image (JPG/PNG)")
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name=_("Available"),
        help_text=_("Whether product is available for purchase")
    )

    stock = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(MIN_STOCK),
            MaxValueValidator(MAX_STOCK)
        ],
        verbose_name=_("Stock"),
        help_text=_("Number of units in warehouse")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated")
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at'])
        ]

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """String rappresentation: product name."""
        return self.name
    
    def get_absolute_url(self):
        """Return the URL for this product detail page."""
        from django.urls import reverse
        return reverse('shop:product-detail', kwargs={'slug': self.slug})
    
    def is_in_stock(self) -> bool:
        """
        Check if product is available and has stock.
    
        Returns:
            bool: True if available and stock > 0
        """
        return self.is_available and self.stock > 0
    
    def can_purchase_quantity(self, quantity: int) -> bool:
        """
        Verify if requested quantity is available.
        
        Args:
            quantity (int): Quantity to purchase
            
        Returns:
            bool: True if quantity is available in stock
        """
        return self.stock >= quantity
    
    def get_display_price(self) -> str:
        """
        Format price for display.

        Returns:
            str: Formatted price (ex: "29.99 EUR")
        """
        return f"{self.price:.2f} EUR"
    
    def increase_stock(self, quantity):
        """Increase product stock."""
        self.stock += quantity
        self.save(update_fields=['stock'])