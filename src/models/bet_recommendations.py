# game_id
# red_side_team_id
# blue_side_team_id
# blue_side_odds
# red_side_odds
# market
# red_side_ev
# blue_side_ev
# red_side_success
# blue_side_success

from src.schema.game import Game
from src.models.mappings import map_team_and_market_to_odds

def _get_market_success(game, side, market, n):
    team = getattr(game, side + '_side_team')
    games = Game.played_by_team_before_date(team, game.date, n)

    return team.market_success_over_games(games, market)


def _calc_ev_for(side, data):
    """
    Calculate EV for a given side

    Parameters:
        side: 'blue' | 'red'
        data: { blue_success: float, red_success: float, blue_odds: float, red_odds: float }

    Returns:
        float: Expected EV
    """

    if side is 'red':
        blue_failure = 1 - data['blue_success']
        return ((data['red_success'] + blue_failure) / 2) * data['red_odds']

    if side is 'blue':
        red_failure = 1 - data['red_success']
        return ((data['blue_success'] + red_failure) / 2) * data['blue_odds']

def market_summary_for_game(game):
    red_success = _get_market_success(game, 'red', 'fbaron', n=14)
    blue_success = _get_market_success(game, 'blue', 'fbaron', n=14)
    red_odds = map_team_and_market_to_odds(game, side='red', market='fbaron')
    blue_odds = map_team_and_market_to_odds(game, side='blue', market='fbaron')

    data = {
            'red_success': red_success,
            'blue_success': blue_success,
            'red_odds': red_odds,
            'blue_odds': blue_odds,
            }

    return {
            **data,
            'red_ev': _calc_ev_for('red', data),
            'blue_ev': _calc_ev_for('blue', data)
            }
