from decimal import Decimal

from simulated_sportsbook.models import Betslip
from users.models import AccountAdjustments, Account


class BetslipsService:
    def __init__(self):
        pass

    def create_betslip(self, data):
        house_account = Account.objects.get(id=1)
        house_starting_balance = house_account.current_balance
        print(f'House balance before wager is placed. | {house_account.current_balance}')

        user_account = data['account']
        starting_balance = user_account.current_balance
        print(f'{user_account.user.username} account value before deducting wager | {user_account.current_balance}')

        stake = data['stake']
        stake = Decimal(stake)
        adjusted_stake_for_user = -abs(stake)

        user_account.current_balance -= Decimal(stake)
        user_account.save()
        print(f'{user_account.user.username} account value after deducting wager | {user_account.current_balance}')

        house_account.current_balance += stake
        house_account.save()
        print(f'House account was incremented by {stake}.')
        print(f'House account value after accepting wager {house_account.current_balance}')

        # Adjustment for the user
        AccountAdjustments.objects.create(
            user_account=user_account,
            previous_balance=int(starting_balance),
            new_balance=user_account.current_balance,
            amount_adjusted=adjusted_stake_for_user,
            notes=f'Bet placed on {data["predicted_outcome"]} in {data["event"]} for {stake} dollars.'
        )
        # Adjustment for the house
        AccountAdjustments.objects.create(
            user_account=house_account,
            previous_balance=int(house_starting_balance),
            new_balance=house_account.current_balance,
            amount_adjusted=stake,
            notes=f'{user_account.user.username} placed a bet on {data["predicted_outcome"]} in {data["event"]} for {stake} dollars.'
        )

        type_of_bet = data['type_of_bet']
        formatted_bet_type = None
        if type_of_bet in ('money line', 'money_line'):
            formatted_bet_type = Betslip.MONEY_LINE
        elif type_of_bet == 'spread':
            formatted_bet_type = Betslip.SPREAD
        elif type_of_bet == 'over_under':
            formatted_bet_type = Betslip.OVER_UNDER
        betslip = Betslip.objects.create(
            user_account=user_account,
            event=data['event'],
            type_of_bet=formatted_bet_type,
            predicted_outcome=data['predicted_outcome'],
            stake=stake,
        )
        print(f'Betslip successfully created for {user_account.user.username.title()}')
        return betslip

    def process_betslip(self, betslip):
        house_account = Account.objects.get(id=1)
        matched_prediction = None
        matched_money_line_price = None
        profit = None
        matched_spread_points = None
        matched_spread_price = None
        event = betslip.event
        account = betslip.user_account
        type_of_bet = betslip.type_of_bet
        stake = betslip.stake

        if event.completed:
            # Who covered the spread?
            home_point_spread = event.spread_home_team_points
            away_point_spread = event.spread_away_team_points
            away_team_points_scored = event.home_team_points_scored
            home_team_points_scored = event.home_team_points_scored
            home_team_difference = home_team_points_scored - home_point_spread
            away_team_difference = away_team_points_scored - away_point_spread

            # If this statement results in a positive number then the home team scored more and there for won.
            if event.home_team_points_scored - event.away_team_points_scored > 0:
                event_winner = event.home_team
            else:
                event_winner = event.away_team

            if betslip.predicted_outcome == event.home_team:
                matched_prediction = event.home_team
                matched_money_line_price = event.home_team_money_line_price
                matched_spread_points = event.spread_home_team_points
                matched_spread_price = event.spread_home_team_price
            elif betslip.predicted_outcome == event.away_team:
                matched_prediction = event.away_team
                matched_money_line_price = event.away_team_money_line_price
                matched_spread_points = event.spread_away_team_points
                matched_spread_price = event.spread_away_team_price
            elif betslip.predicted_outcome == 'Over':
                matched_prediction = 'over'
            elif betslip.predicted_outcome == 'Under':
                matched_prediction = 'under'

            if matched_prediction:
                if type_of_bet == Betslip.MONEY_LINE:
                    if event_winner == matched_prediction:
                        print(f'We got a winner here! {betslip.user_account}')
                        if matched_money_line_price < 0:
                            profit = 100 / abs(matched_money_line_price) * stake
                        elif matched_money_line_price > 0:
                            profit = matched_money_line_price / 100 * stake

                        total_return = profit + stake
                        betslip.profit = profit
                        betslip.total_return = total_return
                        betslip.processed_ticket = True
                        betslip.winning_ticket = True

                        AccountAdjustments.objects.create(
                            user_account=account,
                            previous_balance=account.current_balance,
                            amount_adjusted=total_return,
                            new_balance=account.current_balance + total_return,
                            notes=f'Winnings from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                        )
                        AccountAdjustments.objects.create(
                            user_account=house_account,
                            previous_balance=house_account.current_balance,
                            amount_adjusted=-abs(total_return),
                            new_balance=house_account.current_balance - total_return,
                            notes=f'Payout from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                        )
                        account.current_balance += total_return
                        account.save()

                        house_account.current_balance -= total_return
                        house_account.save()

                        betslip.save()

                    else:
                        print('Better luck next time!')
                        betslip.processed_ticket = True
                        betslip.total_return = 0
                        betslip.profit = 0
                        betslip.save()

                elif type_of_bet == Betslip.SPREAD:
                    # Did they cover?
                    cover = False
                    if home_point_spread == matched_spread_points:
                        if home_team_difference > matched_spread_points:
                            cover = True
                    elif away_point_spread == matched_spread_points:
                        if away_team_difference > matched_spread_points:
                            cover = True

                    if cover:
                        if matched_spread_price < 0:
                            profit = 100 / abs(matched_spread_price) * stake
                        elif matched_spread_price > 0:
                            profit = matched_spread_price / 100 * stake

                        total_return = profit + stake
                        betslip.profit = profit
                        betslip.total_return = total_return
                        betslip.processed_ticket = True
                        betslip.winning_ticket = True

                        AccountAdjustments.objects.create(
                            user_account=account,
                            previous_balance=account.current_balance,
                            amount_adjusted=total_return,
                            new_balance=account.current_balance + total_return,
                            notes=f'Winnings from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                        )
                        AccountAdjustments.objects.create(
                            user_account=house_account,
                            previous_balance=house_account.current_balance,
                            amount_adjusted=-abs(total_return),
                            new_balance=house_account.current_balance - total_return,
                            notes=f'Payout from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                        )
                        account.current_balance += total_return
                        account.save()

                        house_account.current_balance -= total_return
                        house_account.save()

                        betslip.save()
                    else:
                        print('Better luck next time!')
                        betslip.processed_ticket = True
                        betslip.winning_ticket = False
                        betslip.save()

                elif betslip.type_of_bet == Betslip.OVER_UNDER:
                    if betslip.predicted_outcome == 'Over':
                        game_over_under = event.over_under_points
                        game_total_points = event.home_team_points_scored + event.away_team_points_scored
                        if game_total_points > game_over_under:
                            print('We have a winner!')
                            if event.over_price < 0:
                                profit = 100 / abs(event.over_price) * stake
                            elif event.over_price > 0:
                                profit = event.over_price / 100 * stake

                            total_return = profit + stake
                            betslip.profit = profit
                            betslip.total_return = total_return
                            betslip.processed_ticket = True
                            betslip.winning_ticket = True

                            AccountAdjustments.objects.create(
                                user_account=account,
                                previous_balance=account.current_balance,
                                amount_adjusted=total_return,
                                new_balance=account.current_balance + total_return,
                                notes=f'Winnings from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                            )
                            AccountAdjustments.objects.create(
                                user_account=house_account,
                                previous_balance=house_account.current_balance,
                                amount_adjusted=-abs(total_return),
                                new_balance=house_account.current_balance - total_return,
                                notes=f'Payout from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                            )
                            account.current_balance += total_return
                            account.save()
                            house_account.current_balance - total_return
                            house_account.save()
                            betslip.save()
                        else:
                            print('Better luck next time.')
                            betslip.processed_ticket = True
                            betslip.save()
                    elif betslip.predicted_outcome == 'Under':
                        game_over_under = event.over_under_points
                        game_total_points = event.home_team_points_scored + event.away_team_points_scored
                        if game_total_points < game_over_under:
                            print('We have a winner!')
                            if event.under_price < 0:
                                profit = 100 / abs(event.under_price) * stake
                            elif event.under_price > 0:
                                profit = event.under_price / 100 * stake

                                total_return = profit + stake
                                betslip.profit = profit
                                betslip.total_return = total_return
                                betslip.processed_ticket = True
                                betslip.winning_ticket = True

                                AccountAdjustments.objects.create(
                                    user_account=account,
                                    previous_balance=account.current_balance,
                                    amount_adjusted=total_return,
                                    new_balance=account.current_balance + total_return,
                                    notes=f'Winnings from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                                )
                                AccountAdjustments.objects.create(
                                    user_account=house_account,
                                    previous_balance=house_account.current_balance,
                                    amount_adjusted=-abs(total_return),
                                    new_balance=house_account.current_balance - total_return,
                                    notes=f'Payout from betslip ID : {betslip.id} | {betslip.type_of_bet}'
                                )
                                account.current_balance += total_return
                                account.save()
                                house_account.current_balance -= total_return
                                house_account.save()
                                betslip.save()
                        else:
                            print('Better luck next time.')
                            betslip.processed_ticket = True
                            betslip.save()
        else:
            print(f'{event} has not been marked as complete. Try refreshing the results to check if the game '
                  f'has been played.')
