import json
from flask import Blueprint

from src.schema.teams import Team


bp = Blueprint('teams', __name__)


@bp.route('/teams', methods=['GET'])
def teams():
    """
    Return a list of all teams

    Parameters:
        None

    Example:
        curl /teams

    Example response:
        [
          {
            "id" : 116,
            "name" : "Golden Guardians",
            "short_name" : 'ggs'
          }
        ]
    """
    return json.dumps([x.to_json() for x in Team.select()])
