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
    """
    return json.dumps([x.to_json() for x in League.active_leagues()])
