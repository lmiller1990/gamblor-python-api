from flask import Blueprint, request
import json
from playhouse.shortcuts import model_to_dict


from src.schema.league import League


bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def schedule():
    name = request.args.get('league').replace('_', ' ')
    league = League.find_by_name(name)
    split = league.current_split()
    unplayed_games = split.unplayed_games()

    return json.dumps({
        'league': league.id,
        'games': [g.to_json() for g in unplayed_games]
        }, default=str)
