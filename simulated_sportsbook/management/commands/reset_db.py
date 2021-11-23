from django.core.management import BaseCommand, call_command
import django.contrib.auth

from users.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('flush', '--noinput')
        call_command('makemigrations')
        call_command('migrate')
        User = django.contrib.auth.get_user_model()

        house_user = User.objects.create_user(
            email='thehouse@garlichurch.com',
            username='house',
            password='brickhouse',
            is_staff=True,
            is_superuser=True
        )
        house_account = Account.objects.create(
            user=house_user,
        )
        house_user.save()
        house_account.save()
        print(f'{house_user.username.title()} user account was created')

        sam_user = User.objects.create_user(
            email='themeriff@garlichurch.com',
            username='sam',
            password='sports',
            is_staff=True,
            is_superuser=True
        )
        sam_account = Account.objects.create(
            user=sam_user,
        )
        sam_user.save()
        sam_account.save()
        print(f'{sam_user.username.title()}s user account was created')

        katelyn_user = User.objects.create_user(
            email='katelyn@garlichurch.com',
            username='katelyn',
            password='august31',
            is_staff=False,
            is_superuser=False
        )
        katelyn_account = Account.objects.create(
            user=katelyn_user,
        )
        katelyn_user.save()
        katelyn_account.save()
        print(f'{katelyn_user.username.title()}s user account was created')
