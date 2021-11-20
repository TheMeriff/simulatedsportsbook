from django.contrib.auth.models import User

from users.models import Account


class UserAccountService:
    def __init__(self):
        pass

    @staticmethod
    def create_account_association(username):
        user = User.objects.get(username=username)
        user_account = Account.objects.create(user=user)
        
        return user_account
