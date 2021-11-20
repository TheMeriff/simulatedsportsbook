from django.core.management import BaseCommand

from simulated_sportsbook.models import Event
from simulated_sportsbook.services.odds_api_service import OpenApiService
from simulated_sportsbook.tests.fixtures.odds_fixture import mma_events, nba_events, nfl_events


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = OpenApiService()

        for event in nba_events:
            external_event_id = event['id']
            if external_event_id not in service.existing_event_map:
                service.create_event(event, sport=Event.NBA)

        for event in nfl_events:
            external_event_id = event['id']
            if external_event_id not in service.existing_event_map:
                service.create_event(event, sport=Event.NFL)

        for event in mma_events:
            external_event_id = event['id']
            if external_event_id not in service.existing_event_map:
                service.create_event(event, sport=Event.MMA)
