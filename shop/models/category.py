"""
Category Model: Represents a product category.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ..constants import MAX_CATEGORY_NAME_LENGTH

class Category(models.Model):
    """
    Enterprise e-commerce product category model.

    Attributes:
        name (str): Unique category name
        slug (str): URL-friendly identifier (auto-generated from name)
        description (str): Optional category description
        is_active (bool): Whether category is available
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last modification timestamp
    """
    
    name = models.CharField(
        max_length=MAX_CATEGORY_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name=_("Category Name"),
        help_text=_("Ex: Electronics, Clothing, Books")
    )

    slug = models.SlugField(
        max_length=MAX_CATEGORY_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name=_("Slug"),
        default='',
        help_text=_("URL-friendly identifier (auto-generated)")
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Optional category description")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether products in this category are available")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated")
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Return the URL for this category."""
        from django.urls import reverse
        return reverse('shop:category-detail', kwargs={'slug': self.slug})