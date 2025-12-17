from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BudgetForm(forms.ModelForm):
    # rename budget title
    title = forms.CharField(label="Budget Name", max_length=255) 

    class Meta:
        model = Budget
        fields = ["title",  "transaction_type", "limit_amount", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class TransactionForm(forms.ModelForm):
    # Rename transaction title field here
    title = forms.CharField(label="Transaction Title", max_length=255)

    class Meta:
        model = Transaction
        fields = ["title", "amount", "transaction_type", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

