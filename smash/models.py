from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class User(AbstractUser):
    total_billed_credits = models.FloatField(blank=True, null=True, default=0.0)

    def total_credits(self):
        transaction_list = Transaction.objects.filter(user=self)
        return round(transaction_list.aggregate(total_credits=Coalesce(Sum('credits'), 0.0))['total_credits'], 2)


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user"
    )

    credits = models.FloatField()

    purchase_date = models.DateTimeField(
        auto_now_add=True
    )

    def username(self):
        return self.user.username
