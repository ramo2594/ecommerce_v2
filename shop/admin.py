from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""

    list_display = ['name', 'get_category_name', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    
    def get_category_name(self, obj):
        """Custom column: category name."""
        
        return obj.category.name if obj.category else '_'
    get_category_name.short_description = 'Category'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Details', {
            'fields': ('description', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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
    
    fieldsets = (
        (_('Order Info'), {
            'fields': ('order_number', 'user', 'status')
        }),
        (_('Delivery'), {
            'fields': ('shipping_address', 'billing_address')
        }),
        (_('Payment'), {
            'fields': ('payment_method', 'paid')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'get_final_price']
    list_filter = ['order__status', 'created_at']
    search_fields = ['order__order_number', 'product__name']
    
    readonly_fields = ['unit_price', 'created_at', 'updated_at']
    
    def get_final_price(self, obj):
        return f"€{obj.get_final_price():.2f}"
    get_final_price.short_description = 'Total'
