import json
from flask import Blueprint

from src.schema.league import League


bp = Blueprint('greeting', __name__)


@bp.route('/greeting', methods=['GET'])
def greeting():
    return json.dumps({ 'foo': 'bar' })
