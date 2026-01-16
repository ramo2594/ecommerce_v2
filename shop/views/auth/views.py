"""Auth views for registration and login."""
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from shop.forms import RegisterForm, LoginForm


class RegisterView(FormView):
    """User registration view."""
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('shop:product-list')
    
    def form_valid(self, form):
        """Save user and redirect."""
        user = form.save()
        # Auto-login after registration
        login(self.request, user)
        messages.success(self.request, f'Welcome {user.first_name}! Registration completed!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle validation errors."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Registration'
        return context


class LoginView(FormView):
    """User login view."""
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('shop:product-list')
    
    def form_valid(self, form):
        """Authenticate and login user."""
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data.get('remember_me')
        
        # Try to authenticate with username or email
        user = authenticate(self.request, username=username, password=password)
        
        # If username failed, try with email
        if not user:
            try:
                from django.contrib.auth.models import User
                user_obj = User.objects.get(email=username)
                user = authenticate(self.request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(self.request, user)
            
            # Set session timeout if remember_me is checked
            if remember_me:
                self.request.session.set_expiry(1209600)  # 2 weeks
            else:
                self.request.session.set_expiry(0)  # Close browser to logout
            
            messages.success(self.request, f'Welcome {user.first_name}!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username/email or password!')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """Handle validation errors."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        return context


def logout_view(request):
    """Custom logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('shop:product-list')
