"""
OrderItem Model: Represents individual product lines in an order.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from ..constants import MIN_QUANTITY, MAX_QUANTITY

class OrderItem(models.Model):
    """
    Individual product line within an Order.

    Captures product, quantity, and price AT PURCHASE TIME.
    """

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_("Order")
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )

    quantity = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(MIN_QUANTITY),
            MaxValueValidator(MAX_QUANTITY)
        ],
        verbose_name=_("Quantity")
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price")
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
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ['-created_at']

    def __str__(self):
        """String representation."""
        return f"{self.product.name} x{self.quantity}"
    
    def get_final_price(self):
        """Total price for this line item."""
        return self.quantity * self.unit_price
    
    def get_display(self):
        """Template-friendly display"""
        return f"{self.product.name} x {self.quantity} @ €{self.unit_price:.2f}"