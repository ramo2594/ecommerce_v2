"""
Category Model: Represents a product category.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..constants import MAX_CATEGORY_NAME_LENGTH

class Category(models.Model):
    """
    Enterprise e-commerce product category model.
    """
    
    name = models.CharField(
        max_length=MAX_CATEGORY_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name=_("Category Name"),
        help_text=_("Ex: Electronics, Clothing, Books")
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
        help_text=("Whether products in this category are available")
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
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name