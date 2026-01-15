from django.contrib import admin
from ..models import Product
from django.utils.translation import gettext_lazy as _


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
