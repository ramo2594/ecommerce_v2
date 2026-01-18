"""Checkout views for orders."""
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from shop.models import Order, OrderItem, Customer
from shop.services.cart_service import CartService
from shop.forms import CheckoutForm


class CheckoutView(FormView):
    """Checkout page with customer form."""
    template_name = 'checkout/checkout.html'
    form_class = CheckoutForm
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_service = CartService(self.request)
        
        context['cart_items'] = cart_service.get_cart_items()
        context['cart_total'] = cart_service.get_total()
        
        return context
    
    def form_valid(self, form):
        """Process checkout and create order."""
        cart_service = CartService(self.request)
        cart_items = cart_service.get_cart_items()
        
        if not cart_items:
            messages.error(self.request, 'Your cart is empty!')
            return redirect('shop:cart')
        
        # Create customer
        customer, created = Customer.objects.get_or_create(
            email=form.cleaned_data['email'],
            defaults={
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
                'address': form.cleaned_data['address'],
                'postal_code': form.cleaned_data['postal_code'],
                'city': form.cleaned_data['city'],
                'country': form.cleaned_data['country'],
            }
        )
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            user=self.request.user if self.request.user.is_authenticated else None,
            order_number=f"ORD-{Order.objects.count() + 1:06d}",
            notes=form.cleaned_data.get('notes', '')
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                unit_price=item['price']
            )
        
        # Clear cart
        cart_service.clear_cart()
        
        messages.success(self.request, 'Order created successfully!')
        return redirect('shop:order-confirmation', order_number=order.order_number)


class OrderConfirmationView(TemplateView):
    """Order confirmation page."""
    template_name = 'checkout/order_confirmation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            order = Order.objects.get(order_number=kwargs['order_number'])
            context['order'] = order
            context['items'] = order.items.select_related('product').all()
        except Order.DoesNotExist:
            context['error'] = 'Order not found'
        
        return context
