from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator

class Customer(models.Model):
    """
    Customer information model.

    Stores contact and delivery details for orders.
    Used for both authenticated and anonymous customers.
    """

    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First Name"),
        help_text=_("Ex: John")
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last Name"),
        help_text=_("Ex: Kean")
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name=_("Email"),
        help_text=_("Ex: john@example.com")
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone Number"),
        help_text=_("Optional phone number")
    )
    
    address = models.TextField(
        verbose_name=_("Street Address"),
        help_text=_("Full street address")
    )

    postal_code = models.CharField(
        max_length=20,
        verbose_name=_("Postal Code"),
        help_text=_("ZIP or postal code")
    )

    city = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("City"),
        help_text=_("City name")
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        help_text=_("Country name")
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
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['city']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        """String representation: customer full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_full_name(self) -> str:
        """
        Get customer's full name.
        
        Returns:
            str: Full name (first_name + last_name)
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_full_address(self) -> str:
        """
        Get customer's full address.
        
        Returns:
            str: Full formatted address
        """
        return f"{self.address} {self.postal_code} {self.city} {self.country}"
