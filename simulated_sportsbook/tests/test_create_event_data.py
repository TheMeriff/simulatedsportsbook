from django.test import TestCase

from simulated_sportsbook.models import Event
from simulated_sportsbook.services.odds_api_service import OpenApiService
from simulated_sportsbook.tests.fixtures.odds_fixture import mma_events, nba_events, nfl_events


class EventCreationTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.mma_json = mma_events
        cls.nfl_json = nfl_events
        cls.nba_json = nba_events

    def test_create_events(self):
        events = []
        service = OpenApiService()
        for event in self.nba_json:
            external_event_id = event['id']
            if external_event_id not in service.existing_event_map:
                game = service.create_event(event, sport=Event.NBA)
                events.append(game)

        for event in self.nfl_json:
            external_event_id = event['id']
            if external_event_id not in service.existing_event_map:
                game = service.create_event(event, sport=Event.NFL)
                events.append(game)

        for event in self.mma_json:
            external_event_id = event['id']
            if external_event_id not in service.existing_event_map:
                game = service.create_event(event, sport=Event.MMA)
                events.append(game)
