import json
from flask import Blueprint

from src.schema.split import Split


bp = Blueprint('splits', __name__)


@bp.route('/splits', methods=['GET'])
def splits():
    """
    Return a list of all active splits

    Parameters:
        None

    Example:
        curl /splits

    Example response:
        [
           {
              "created_at" : "2019-04-30 08:24:08",
              "id" : 12,
              "league_id" : 10,
              "name" : "All Games"
           }
        ]
    """
    return json.dumps([x.to_json() for x in Split.select()])
