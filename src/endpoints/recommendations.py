import json
from flask import Blueprint, request
from datetime import datetime, timedelta

from src.schema.split import Split
from src.models.bet_recommendations import get_recommendations_for_unplayed_games


bp = Blueprint('recommendations', __name__)


@bp.route('/recommendations', methods=['GET'])
def recommendations():
    from src.schema.game import Game
    """
    """
    past_n_games = int(request.args.get('past_n_games'))

    if past_n_games is None:
        raise ValueError('market and past_n_games query parameters are required')

    four_days_ago = datetime.now() - timedelta(days=4)
    games = Game.unplayed(since=four_days_ago)
    summary = get_recommendations_for_unplayed_games(games, past_n_games)

    return json.dumps(summary)
