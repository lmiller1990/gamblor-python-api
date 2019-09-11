import json
from flask import Blueprint, request
from datetime import datetime, timedelta

from src.schema.game import Game
from src.models.bet_recommendations import get_recommendations_for_unplayed_games


bp = Blueprint('recommendations', __name__)


@bp.route('/recommendations', methods=['GET'])
@bp.route('/api/recommendations', methods=['GET'])
def recommendations():
    """
    Return a list of recommendations for upcoming games, including EV, success rate, etc.

    Parameters:
        past_n_games (int): number of games to consider in EV calculation
        game_ids (int[]): games to retreive recommendations for

    Example:
        curl /recommendations?past_n_games=20

    Example response:
        [
            {
              "blue_ev" : 0.605,
              "blue_odds" : 2.2,
              "blue_side_team_id" : 119,
              "blue_success" : 0.4,
              "game_id": 1,
              "market" : "fd",
              "red_ev" : 1.16725,
              "red_odds" : 1.61,
              "red_side_team_id" : 4,
              "red_success" : 0.85
           }
       ]
    """
    if request.args.get('game_ids') is '':
        return json.dumps([])

    ids = request.args.get('game_ids').split(',')
    game_ids = list(map(int, ids))
    past_n_games = int(request.args.get('past_n_games'))

    if past_n_games is None:
        raise ValueError('market and past_n_games query parameters are required')

    games = Game.select().where(Game.id.in_(game_ids))
    summary = get_recommendations_for_unplayed_games(games, past_n_games)

    return json.dumps(summary)
