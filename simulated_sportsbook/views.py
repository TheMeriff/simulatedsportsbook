from django.http import HttpResponse
from django.shortcuts import render

from simulated_sportsbook.models import Event, Betslip
from simulated_sportsbook.services.betslips import BetslipsService
from simulated_sportsbook.services.odds_api_service import OpenApiService
from simulated_sportsbook.services.results_service import ResultsService


def index(request):
    nba_events = Event.objects.filter(sport=Event.NBA).order_by('start_time')
    nfl_events = Event.objects.filter(sport=Event.NFL).order_by('start_time')
    mma_events = Event.objects.filter(sport=Event.MMA).order_by('start_time')

    context = {
        'nba_events': nba_events,
        'nfl_events': nfl_events,
        'mma_events': mma_events,
    }

    return render(request, 'index.html', context=context)


def refresh_odds(request):
    context = {}
    nba_events = None
    nfl_events = None
    mma_events = None
    if request.method == 'POST':
        try:
            nba_refresh = request.POST.get('nba_refresh')
            nfl_refresh = request.POST.get('nfl_refresh')
            mma_refresh = request.POST.get('mma_refresh')
            process_betslips = request.POST.get('process_betslips')
            if nba_refresh == 'on':
                # Pull in new odds
                nba_events = OpenApiService().get_nba_odds()
                # Update existing NBA events with scores
                ResultsService.process_nba_events()
            if nfl_refresh == 'on':
                nfl_events = OpenApiService().get_nfl_odds()
            if mma_refresh == 'on':
                mma_events = OpenApiService().get_mma_odds()
            if process_betslips == 'on':
                betslip = Betslip.objects.get(id=1)
                BetslipsService().process_betslip(betslip)
            context = {'nba_events': nba_events, 'nfl_events': nfl_events, 'mma_events': mma_events}
        except Exception as e:
            return HttpResponse(e)

    return render(request, 'refresh_odds.html', context=context)
