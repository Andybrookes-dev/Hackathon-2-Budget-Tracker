from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

# Create your models here.



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("rent", "Rent"),
        ("utilities", "Utilities"),
        ("groceries", "Groceries"),
        ("savings", "Savings"),
        ("entertainment", "Entertainment"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.transaction_type})"


class Budget(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgets"
    )
    transaction_type = models.CharField(
    max_length=20,
    choices=Transaction.TRANSACTION_TYPES,
    null=True,
    blank=True,
   )

    title = models.CharField(max_length=255)
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

   
    @property
    def spent_amount(self):
        return (
            self.user.transactions.filter(
                transaction_type=self.transaction_type,
                date__gte=self.start_date,
                date__lte=self.end_date,
            ).aggregate(total=models.Sum("amount"))["total"]
            or Decimal("0.00")
        )

    @property
    def remaining_amount(self):
        return self.limit_amount - self.spent_amount

    @property
    def is_over_limit(self):
        return self.spent_amount > self.limit_amount

