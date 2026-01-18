"""
Order Model: Represents customer orders.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from decimal import Decimal
from ..constants import ORDER_STATUS_CHOICES

class Order(models.Model):
    """
    Order model representing a customer purchase.

    Can be associated with an authenticated user or be anonymous.
    Stores order details, customer info, and payment status.
    """

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_("User"),
        help_text=_("Authenticated user who placed the order")
    )

    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_("Customer"),
        help_text=_("Customer information")
    )

    order_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("Order Number"),
        help_text=_("Unique order identifier")
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        db_index=True,
        verbose_name=_("Status"),
        help_text=_("Current order status")
    )

    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Tax Amount"),
        help_text=_("Tax amount in EUR")
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Shipping Cost"),
        help_text=_("Shipping cost in EUR")
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Optional order notes or special requests")
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
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-created_at'])
        ]
    
    def __str__(self):
        """String representation: order number."""
        return f"Order #{self.order_number}"
    
    def get_absolute_url(self):
        """Return the URL for this order detail page."""
        from django.urls import reverse
        return reverse('shop:order-detail', kwargs={'order_number': self.order_number})
    
    def get_total_price(self):
        """Calculate total order price."""
        return sum(item.get_final_price() for item in self.items.all())
    
    def get_status_display(self):
        """Return human-readable status."""
        return dict(ORDER_STATUS_CHOICES)[self.status]
    
    def is_recently_created(self):
        """Check if order was created in the last 7 days"""
        from django.utils import timezone
        return (timezone.now() - self.created_at) < timezone.timedelta(days=7)
    
    def cancel(self):
        """Cancel this order and restore product stock."""
        if self.status != 'pending':
            return False
        
        self.status = 'cancelled'
        self.save(update_fields=['status'])

        # Restore stock
        for item in self.items.all():
            item.product.increase_stock(item.quantity)

        return True
    
@property
def items(self):
    """Returns order items with products prefetch."""
    return self.orderitem_set.select_related('product').all()

