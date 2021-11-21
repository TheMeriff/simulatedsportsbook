from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    starting_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=500.00)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=500.00)

    def __str__(self):
        return f'id: {self.id} | {self.user.username} | {self.current_balance}'


class AccountAdjustments(models.Model):
    user_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='adjustments')
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_adjusted = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f'id: {self.id} | Account adjustments for{self.user_account.user.username}'
