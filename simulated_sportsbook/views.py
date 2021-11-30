from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from simulated_sportsbook.models import Event, Betslip
from simulated_sportsbook.services.betslips import BetslipsService
from simulated_sportsbook.services.odds_api_service import OpenApiService
from simulated_sportsbook.services.results_service import ResultsService
from users.models import Account, AccountAdjustments
from users.services.user_account_service import UserAccountService


def index(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    if request.method == 'POST':
        try:
            events = Event.objects.all().exclude(completed=True)
            for event in events:
                if request.POST.get(event.external_id):
                    data = {}
                    user_account = Account.objects.get(user=request.user)
                    # Validate user balance for bet
                    user_account_balance = user_account.current_balance
                    wager = Decimal(request.POST.get(f'{event.external_id} | amount_wagered'))
                    if Decimal(wager) <= user_account_balance:
                        type_of_bet = request.POST.get(event.external_id)
                        predicted_outcome = request.POST.get(f'{event.external_id} | predicted_outcome')
                        data['account'] = user_account
                        data['event'] = event
                        data['type_of_bet'] = type_of_bet
                        data['predicted_outcome'] = predicted_outcome
                        if type_of_bet in ('money line', 'spread') and predicted_outcome in ('Over', 'Under'):
                            messages.error(request, f'You are not allowed to bet {predicted_outcome} on {type_of_bet.title()}.')
                            return redirect('index')
                        data['stake'] = wager
                        BetslipsService().create_betslip(data)
                        messages.success(request, f'Betslip Created Successfully!')
                        return redirect('index')
                    else:
                        messages.error(request, f'Wager of {wager} exceeds your account balance of {user_account_balance}, Betslip was not created.')
                        return redirect('index')
        except Exception as e:
            render(request, e)
    else:
        now = datetime.utcnow() - timedelta(hours=6)
        house_account = Account.objects.get(id=1)
        house_balance = house_account.current_balance
        username = request.user.username
        user_account = Account.objects.get(user=request.user)
        current_balance = user_account.current_balance
        nba_events = Event.objects.filter(sport=Event.NBA).order_by('start_time').exclude(completed=True).exclude(start_time__lt=now)
        nfl_events = Event.objects.filter(sport=Event.NFL).order_by('start_time').exclude(completed=True).exclude(start_time__lt=now)
        mma_events = Event.objects.filter(sport=Event.MMA).order_by('start_time').exclude(completed=True).exclude(start_time__lt=now)
        custom_events = Event.objects.filter(sport=Event.CUSTOM).order_by('start_time').exclude(completed=True).exclude(start_time__lt=now)
        leaderboard_data = Account.objects.all().order_by('-current_balance')
        leaderboard = {}
        for player in leaderboard_data[:5]:
            pending_bets = Betslip.objects.filter(user_account=player).exclude(processed_ticket=True)
            leaderboard[player.user.username.title()] = {
                'current_balance': player.current_balance,
                'pending_bets': pending_bets.count(),
                'username': player.user.username.title()
            }
        user_betslips = Betslip.objects.filter(user_account=user_account)
        total_betslips = len(user_betslips)
        processed_betslips = user_betslips.exclude(processed_ticket=False)
        winning_tickets = processed_betslips.filter(winning_ticket=True)
        if winning_tickets and processed_betslips:
            winning_percent = winning_tickets.count() / processed_betslips.count()
        else:
            winning_percent = None
        losing_tickets = processed_betslips.exclude(winning_ticket=True)
        pending_betslips = user_betslips.filter(processed_ticket=False)

        largest_bet = 0
        for bet in user_betslips:
            if bet.stake > largest_bet:
                largest_bet = bet.stake

        context = {
            'account': user_account,
            'nba_events': nba_events,
            'nfl_events': nfl_events,
            'mma_events': mma_events,
            'custom_events': custom_events,
            'username': username,
            'current_balance': current_balance,
            'house_balance': house_balance,
            'leaderboard': leaderboard,
            'total_betslips': total_betslips or 0,
            'processed_betslips': len(processed_betslips) if processed_betslips else None,
            'num_processed_betslips': len(processed_betslips) if processed_betslips else '0',
            'pending_betslips': len(pending_betslips) if pending_betslips else None,
            'winning_percent': winning_percent * 100 if winning_tickets else 'Not available yet.',
            'winning_tickets': len(winning_tickets) if winning_tickets else None,
            'num_winning_tickets': len(winning_tickets) if winning_tickets else '0',
            'losing_tickets': len(losing_tickets) if losing_tickets else None,
            'largest_bet': largest_bet,
            'num_total_users': leaderboard_data.count()
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
                ResultsService.process_nfl_events()
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
    user_betslips = Betslip.objects.filter(user_account=user_account)
    total_betslips = len(user_betslips)
    processed_betslips = user_betslips.exclude(processed_ticket=False)
    winning_tickets = processed_betslips.filter(winning_ticket=True)
    if winning_tickets and processed_betslips:
        winning_percent = winning_tickets.count() / processed_betslips.count()
    else:
        winning_percent = None
    losing_tickets = processed_betslips.exclude(winning_ticket=True)
    num_losing_tickets = losing_tickets.count()
    pending_betslips = user_betslips.filter(processed_ticket=False)

    largest_bet = 0
    for bet in user_betslips:
        if bet.stake > largest_bet:
            largest_bet = bet.stake

    context = {
        'username': username.title(),
        'account': user_account,
        'adjustments': adjustments,
        'total_betslips': total_betslips,
        'num_processed_betslips': len(processed_betslips) if processed_betslips else 0,
        'num_winning_tickets': len(winning_tickets) if winning_percent else 0,
        'win_percent': winning_percent * 100 if winning_percent else 'Not Available',
        'largest_bet': largest_bet,
        'losing_tickets': losing_tickets,
        'winning_tickets': winning_tickets,
        'num_losing_tickets': str(num_losing_tickets),
        'num_pending_betslips': str(len(pending_betslips)) if pending_betslips else None,
        'pending_betslips': pending_betslips
    }

    if request.method == 'POST':
        account_reset = request.POST.get('account_reset_true')
        if account_reset:
            pending_betslips = Betslip.objects.filter(user_account__user=request.user)
            if pending_betslips:
                messages.error(request, 'You are not allowed to reset your balance while you still have pending betslips.')
                return render(request, 'account.html', context=context)
            UserAccountService().reset_account_balance(request.user)
            messages.success(request, 'Account Balance reset to 500')
            return render(request, 'account.html', context=context)
        else:
            messages.error(request, 'Check the box if you and hit the red button if you want to reset your account.')
            return render(request, 'account.html', context=context)
    else:
        if request.user.is_anonymous:
            return redirect("/login/")

        return render(request, 'account.html', context=context)
