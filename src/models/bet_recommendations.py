import itertools
from src.utils.datetime import stringify_date

from src.types import markets
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

def market_summary_for_game(game, market, past_n_games):
    """
    Summarizes the markets for a given game

    Parameters:
        game: schema.Game to summarizes markets for
        market: 'fb' | 'ft' | 'fd' | 'fbaron'
        past_n_games: the number of prior games to consider when calculating the EV


    Returns:
        dictionary: { 
            market: 'fb' | 'ft' | 'fd' | 'fbaron',
            date: string,
            id: string,
            red_success: float, 
            blue_success: float, 
            red_odds: float, 
            blue_odds: float,
            red_ev: float,
            blue_ev: float
            red_side_team_id: int,
            blue_side_team_id: int
        }
    """
    red_success = _get_market_success(game, 'red', market, n=past_n_games)
    blue_success = _get_market_success(game, 'blue', market, n=past_n_games)
    red_odds = map_team_and_market_to_odds(game, side='red', market=market)
    blue_odds = map_team_and_market_to_odds(game, side='blue', market=market)

    data = {
            'red_success': red_success,
            'blue_success': blue_success,
            'red_odds': red_odds,
            'blue_odds': blue_odds,
            }

    return {
            **data,
            'id': str(game.id) + '-' + market,
            'date': stringify_date(game.date),
            'market': market,
            'game_id': game.id,
            'red_side_team_id': game.red_side_team_id,
            'blue_side_team_id': game.blue_side_team_id,
            'red_ev': _calc_ev_for('red', data),
            'blue_ev': _calc_ev_for('blue', data)
            }

def market_summaries_for_game(game, past_n_games):
    """
    Summarize all markets for a given game, and return results 

    Parameters:
        game: schema.Game,
        past_n_games: number of previous games

    Returns:
        A list of dictionaries, see return type of market_summary_for_game above
    """
    return [market_summary_for_game(game, market, past_n_games) for market in markets]


def get_recommendations_for_unplayed_games(games, past_n_games):
    """
    Return summaries for a set of games

    Parameters:
        games: schema.Game[]
        past_n_games: how many previous games to consider in EV calculation

    Returns:
        A list of dictionaries of recommendations. See return type of market_summary_for_game above
    """
    summaries = [market_summaries_for_game(game, past_n_games) for game in games]
    return [x for y in summaries for x in y]
