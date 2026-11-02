from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to GrX Parfums, {user.first_name or user.email}! Your account is now active.')
            return redirect('catalog:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    next_url = request.GET.get('next') or request.POST.get('next') or 'catalog:home'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('catalog:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile details have been updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    # Fetch user's recent orders
    orders = request.user.orders.all().order_by('-created_at')[:5]

    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders
    })
