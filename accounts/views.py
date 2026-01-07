from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from .models import User



# =====================
# Login (only active users)
# =====================
class LoginView(View):
    template_name = 'autho/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "Your account is not active. Please verify your email.")
                return render(request, self.template_name, {'form': form})
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')
        return render(request, self.template_name, {'form': form})


# =====================
# Logout
# =====================
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('login')


# =====================
# Password Change (Logged-in user)
# =====================
class PasswordChangeView(View):
    template_name = 'autho/password_change.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Password changed successfully!")
            return redirect('income-list')
        return render(request, self.template_name, {'form': form})
