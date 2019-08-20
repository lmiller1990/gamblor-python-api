import json
from flask import Blueprint, request

from src.schema.split import Split
from src.models.bet_recommendations import market_summary_for_game


bp = Blueprint('recommendations', __name__)


@bp.route('/recommendations', methods=['GET'])
def recommendations():
    from src.schema.game import Game
    """
    """
    market = request.args.get('market')
    past_n_games = int(request.args.get('past_n_games'))

    if market is None or past_n_games is None:
        raise ValueError('market and past_n_games query parameters are required')

    summary = market_summary_for_game(Game.get_by_id(1128), market=market, past_n_games=past_n_games)
    return json.dumps(summary)
