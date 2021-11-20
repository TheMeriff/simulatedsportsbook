from django.core.management import BaseCommand, call_command
import django.contrib.auth

from users.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('flush', '--noinput')
        call_command('makemigrations')
        call_command('migrate')
        User = django.contrib.auth.get_user_model()
        user = User.objects.create_user(
            email='themeriff@garlichurch.com',
            username='sam',
            password='sports',
            is_staff=True,
            is_superuser=True
        )
        account = Account.objects.create(
            user=user,
        )
        user.save()
        account.save()
        print(f'{user.username}s user account was created')
