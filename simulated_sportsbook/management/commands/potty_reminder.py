from django.core.management import BaseCommand

from simulated_sportsbook.services.telegram_service import TelegramService


class Command(BaseCommand):
    def handle(self, *args, **options):
        TelegramService().send_potty_reminder()
