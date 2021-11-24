from django.core.management import BaseCommand

from simulated_sportsbook.models import Betslip
from simulated_sportsbook.services.betslips import BetslipsService


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = BetslipsService()
        betslips_to_process = Betslip.objects.filter(processed_ticket=False)
        for betslip in betslips_to_process:
            service.process_betslip(betslip)
