from django.test import TestCase
from django.utils import timezone
from .models import User, Transaction, Budget

# Create your tests here.
class BudgetModelTests(TestCase):
    """
    Tests for the Budget model.
    """   
    def setUp(self):
        self.user = User.objects.create(username="al", email="al@example.com")
        self.budget = Budget.objects.create(
            user=self.user,
            title="December Budget",
            limit_amount=100,
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        Transaction.objects.create(
            user=self.user,
            title="Food shopping",
            amount=35,
            transaction_type="groceries",
            date=timezone.now().date()
        )
