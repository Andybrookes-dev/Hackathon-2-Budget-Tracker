from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'track/index.html')

def login_view(request):
    return render(request, 'track/login.html')

def register_view(request):
    return render(request, 'track/register.html')

def budget_view(request):
    return render(request, 'track/budget.html')
