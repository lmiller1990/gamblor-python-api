import json
from flask import Blueprint

from src.schema.league import League


bp = Blueprint('leagues', __name__)


@bp.route('/leagues', methods=['GET'])
def leagues():
    """
    Return a list of all active leagues

    Parameters:
        None

    Example:
        curl /leagues

    Example response:
        [
           {
              "active" : true,
              "id" : 2,
              "name" : "NA LCS 2019"
           }
        ]
    """
    return json.dumps([x.to_json() for x in League.active_leagues()])
