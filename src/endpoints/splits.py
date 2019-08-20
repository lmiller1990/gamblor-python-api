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
    """
    return json.dumps([x.to_json() for x in Split.select()])
