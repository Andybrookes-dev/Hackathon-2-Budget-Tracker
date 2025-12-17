from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .form import UserRegisterForm
from django.contrib import messages



# Create your views here.

def home(request):
    return render(request, 'track/index.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'track/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('budget')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'track/login.html')


def logout_view(request):
    """User logout view that handles user logout and redirects to home page."""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")

def budget_view(request):
    return render(request, 'track/budget.html')
