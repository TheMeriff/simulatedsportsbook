from django.contrib.auth.models import User

from users.models import Account


class UserAccountService():
    def __init__(self):
        pass

    @staticmethod
    def create_account_association(username):
        user = User.objects.get(username=username)
        user_account = Account.objects.create(user=user)
        
        return user_account

    @staticmethod
    def reset_account_balance(user):
        user_account = Account.objects.get(user=user)
        user_account.account_resets += 1
        user_account.current_balance = 500.00
        user_account.save()
        print(f"{user_account.user.username.title()}'s account balance reset to 500")
        print(f"{user_account.user.username.title()} now has {user_account.account_resets} account resets.")
