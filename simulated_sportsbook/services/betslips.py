from simulated_sportsbook.models import Betslip
from users.models import AccountAdjustments


class BetslipsService:
    def __init__(self):
        pass

    def process_betslip(self, betslip):
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

            if matched_prediction:
                if type_of_bet == Betslip.MONEY_LINE:
                    if event_winner == matched_prediction:
                        print('We got a winner here!')
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
                        account.current_balance += total_return
                        betslip.save()
                        account.save()

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
                        account.current_balance += total_return
                        betslip.save()
                        account.save()
                    else:
                        betslip.processed_ticket = True
                        betslip.winning_ticket = False
                        betslip.save()

                elif betslip.type_of_bet == Betslip.OVER_UNDER:
                    if betslip.predicted_outcome == 'over':
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
                                account.current_balance += total_return
                                betslip.save()
                                account.save()
                        else:
                            print('Better luck next time.')
                            betslip.processed_ticket = True
                            betslip.save()
                    elif betslip.predicted_outcome == 'under':
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
                                account.current_balance += total_return
                                betslip.save()
                                account.save()
                        else:
                            print('Better luck next time.')
                            betslip.processed_ticket = True
                            betslip.save()