from datetime import datetime, timedelta

from django.core.management import BaseCommand

from simulated_sportsbook.services.results_service import ResultsService


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = ResultsService()
        service.process_nba_events()
