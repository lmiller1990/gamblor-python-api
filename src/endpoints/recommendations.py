import json
from flask import Blueprint

from src.schema.split import Split
from src.models.bet_recommendations import market_summary_for_game


bp = Blueprint('recommendations', __name__)


@bp.route('/recommendations', methods=['GET'])
def recommendations():
    from src.schema.game import Game
    """
    """
    summary = market_summary_for_game(Game.get_by_id(1128))
    return json.dumps(summary)
