"""
User orders views - Enterprise modular structure
"""
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ...models.order import Order

class UserOrdersListView(LoginRequiredMixin, ListView):
    """
    Display logged-in user orders with optimized queries.
    """
    template_name = 'orders/user_orders_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).select_related('customer').prefetch_related(
            'items__product'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_orders'] = self.get_queryset().count()
        return context
