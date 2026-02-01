from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('blog:home')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'Email not registered')
    return render(request, 'accounts/login.html')

@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='accounts:login')
def user_posts(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('blog:home')
    
    posts = user.blog_posts.filter(status='published').order_by('-published_at')
    context = {
        'author': user,
        'posts': posts,
    }
    return render(request, 'accounts/user_posts.html', context)

@login_required(login_url='accounts:login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('blog:home')
