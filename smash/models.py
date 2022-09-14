from django.contrib.auth.models import User
from django.db import models


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




