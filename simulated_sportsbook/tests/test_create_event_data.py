from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from simulated_sportsbook.models import Event, Betslip
from simulated_sportsbook.services.betslips import BetslipsService
from simulated_sportsbook.services.odds_api_service import OpenApiService
from simulated_sportsbook.services.results_service import ResultsService
from simulated_sportsbook.tests.fixtures.odds_fixture import mma_events, nba_events, nfl_events
from users.models import Account


class EventCreationTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.mma_json = mma_events
        cls.nfl_json = nfl_events
        cls.nba_json = nba_events
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

        cls.user = user
        cls.account = account

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

        money_line_betslip = Betslip.objects.create(
            user_account=self.account,
            type_of_bet=Betslip.MONEY_LINE,
            event=events[27],
            stake=Decimal('100'),
            predicted_outcome='Tampa Bay Buccaneers'
        )
        spread_betslip = Betslip.objects.create(
            user_account=self.account,
            type_of_bet=Betslip.SPREAD,
            event=events[27],
            stake=Decimal('100'),
            predicted_outcome='Tampa Bay Buccaneers'
        )
        over_under_betslip = Betslip.objects.create(
            user_account=self.account,
            type_of_bet=Betslip.OVER_UNDER,
            event=events[27],
            stake=Decimal('100'),
            predicted_outcome='Over'
        )

        ResultsService().process_nfl_events()

        processed_betslips = Betslip.objects.all()
        for betslip in processed_betslips:
            BetslipsService().process_betslip(betslip)



