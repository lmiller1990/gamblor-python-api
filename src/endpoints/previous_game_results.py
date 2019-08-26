import json
from flask import Blueprint, request

from src.schema.teams import Team


bp = Blueprint('previous_game_results', __name__)


@bp.route('/previous_game_results', methods=['GET'])
def previous_game_results():
    """
    Return a list of results of previous games for a team

    Parameters:
        team_id: team_id to return game results for
        n: number of previous games

    Example:
        curl /previous_game_results?team_id=1&n=10

    Example response:
        [
           {
              "fb" : false,
              "fbaron" : false,
              "fd" : true,
              "ft" : false,
              "game_id" : 809,
              "date": game.date,
              "team_id": self.id,
              "opponent_id": opponent_id,
              "win" : false
           }
        ]
    """
    team_id = int(request.args.get('team_id'))
    n = int(request.args.get('n'))

    if team_id is None or n is None:
        raise ValueError('team_id query parameter is required')

    team = Team.get_by_id(int(team_id))
    games = team.results_for_previous_games(n=n)

    return json.dumps(games)
