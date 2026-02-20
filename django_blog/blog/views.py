from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        # Simple update: only email here
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, "Profile updated!")
    return render(request, 'blog/profile.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
