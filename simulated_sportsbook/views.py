from django.http import HttpResponse
from django.shortcuts import render, redirect

from simulated_sportsbook.models import Event, Betslip
from simulated_sportsbook.services.betslips import BetslipsService
from simulated_sportsbook.services.odds_api_service import OpenApiService
from simulated_sportsbook.services.results_service import ResultsService
from users.models import Account, AccountAdjustments


def index(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    username = request.user.username
    nba_events = Event.objects.filter(sport=Event.NBA).order_by('start_time').exclude(completed=True)
    nfl_events = Event.objects.filter(sport=Event.NFL).order_by('start_time').exclude(completed=True)
    mma_events = Event.objects.filter(sport=Event.MMA).order_by('start_time').exclude(completed=True)

    context = {
        'nba_events': nba_events,
        'nfl_events': nfl_events,
        'mma_events': mma_events,
        'username': username,
    }

    return render(request, 'index.html', context=context)


def refresh_odds(request):
    if request.user.is_anonymous:
        return redirect("/login/")
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
                betslips = Betslip.objects.all().exclude(processed_ticket=True)
                for betslip in betslips:
                    BetslipsService().process_betslip(betslip)
            context = {'nba_events': nba_events, 'nfl_events': nfl_events, 'mma_events': mma_events}
        except Exception as e:
            return HttpResponse(e)

    return render(request, 'refresh_odds.html', context=context)


def account(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    user = request.user
    username = request.user.username
    user_account = Account.objects.get(user=user)
    adjustments = AccountAdjustments.objects.filter(user_account=user_account)
    context = {
        'username': username.title(),
        'account': user_account,
        'adjustments': adjustments
    }

    return render(request, 'account.html', context=context)
