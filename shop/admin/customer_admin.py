from django.contrib import admin
from ..models import Customer
from django.utils.translation import gettext_lazy as _


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model."""
    
    list_display = ['get_full_name', 'email', 'city', 'country', 'created_at']
    list_filter = ['city', 'country', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'postal_code', 'city', 'country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def get_full_name(self, obj):
        """Custom column: full name."""
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
