from django.contrib import admin
from ..models import Order, OrderItem
from django.utils.translation import gettext_lazy as _

class OrderItemInline(admin.TabularInline):
    """Inline OrderItem display."""
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'created_at', 'updated_at']
    
    def get_final_price(self, obj):
        return f"€{obj.get_final_price():.2f}"
    get_final_price.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    
    list_display = [
        'order_number', 
        'user', 
        'get_total_price', 
        'status', 
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        (_('Order Info'), {
            'fields': ('order_number', 'user', 'status')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_total_price(self, obj):
        """Total price display."""
        return f"€{obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'get_final_price']
    list_filter = ['order__status', 'created_at']
    search_fields = ['order__order_number', 'product__name']
    
    readonly_fields = ['unit_price', 'created_at', 'updated_at']
    
    def get_final_price(self, obj):
        return f"€{obj.get_final_price():.2f}"
    get_final_price.short_description = 'Total'
