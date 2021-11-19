from django.http import HttpResponse
from django.shortcuts import render

from simulated_sportsbook.models import Event
from simulated_sportsbook.services.odds_api_service import OpenApiService


def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', context={'events': events})


def nfl_odds(request):
    event = OpenApiService().get_nfl_odds()
    return HttpResponse('Update Successful')


def nba_odds(request):
    event = OpenApiService().get_nba_odds()
    return HttpResponse('Update Successful')
