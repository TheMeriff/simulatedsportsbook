from django.core.management import BaseCommand

from simulated_sportsbook.services.odds_api_service import OpenApiService


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = OpenApiService()
        service.get_mlb_odds()
