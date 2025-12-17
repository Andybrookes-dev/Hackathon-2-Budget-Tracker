from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .form import TransactionForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .form import *
from django.db.models import Sum



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


@login_required
def budget_view(request):
   
    if request.method == "POST":
        budget_form = BudgetForm(request.POST)
        transaction_form = TransactionForm(request.POST)

        if budget_form.is_valid() and transaction_form.is_valid():
            budget = budget_form.save(commit=False)
            transaction = transaction_form.save(commit=False)

            budget.user = request.user
            transaction.user = request.user

            budget.save()
            transaction.save()

            return redirect("dashboard")

    else:
        budget_form = BudgetForm()
        transaction_form = TransactionForm()

    return render(
        request,
        "track/budget.html",
        {
            "budget_form": budget_form,
            "transaction_form": transaction_form,
        },
    )

@login_required
def dashboard_view(request):
  
    user = request.user
    budgets = Budget.objects.filter(user=user)
    transactions = Transaction.objects.filter(user=user).order_by("-date")

    # 🔹 Total amount grouped by transaction_type
    transaction_summary = (
        Transaction.objects
        .filter(user=user)
        .values("transaction_type")
        .annotate(total_amount=Sum("amount"))
    )

    return render(
        request,
        "track/dashboard.html",
        {
            "budgets": budgets,
            "transactions": transactions,
            "transaction_summary": transaction_summary,
        },
    )

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect("dashboard")  # replace with your transaction list view
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "track/edit_transaction.html", {"form": form})
@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    return redirect("dashboard")

