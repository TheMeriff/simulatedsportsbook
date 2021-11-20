from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    starting_balance = models.IntegerField(blank=False, null=False, default=500)
    current_balance = models.IntegerField(blank=False, null=False, default=500)

    def __str__(self):
        return f'id: {self.id} | {self.user.username} | {self.current_balance}'


class AccountAdjustments(models.Model):
    user_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='adjustments')
    previous_balance = models.IntegerField()
    new_balance = models.IntegerField()
    amount_adjusted = models.IntegerField()
    notes = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f'id: {self.id} | Account adjustments for{self.user_account.user.username}'

