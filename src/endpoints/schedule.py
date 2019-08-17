from flask import Blueprint, request
import json

from src.schema.league import League


bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def schedule():
    league_name = request.args.get('league').replace('_', ' ')
    league = League.select().where(League.name == league_name).first()

    return json.dumps({'league': league.id})
