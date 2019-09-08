import json
from flask import Blueprint, request

from src.schema.teams import Team


bp = Blueprint('team_rankings', __name__)


@bp.route('/team_rankings', methods=['GET'])
@bp.route('/api/team_rankings', methods=['GET'])
def team_rankings():
    """
    Return a list of teams win rate over last n games

    Parameters:
        past_n_games (int): number of games to consider win ratio calculation
        league_id (int): league for the teams you are interested in

    Example:
        curl /team_rankings?past_n_games=10&league_id=1

    Example response:
        [
          {
            "id" : 116,
            "name" : "Golden Guardians",
            "short_name" : "ggs",
            "winrate": 0.5,
            "past_n_games": 10
          }
        ]
    """
    past_n_games = int(request.args.get('past_n_games'))
    league_id = int(request.args.get('league_id'))

    if past_n_games is None or league_id is None:
        raise ValueError('past_n_games and league_id query parameters are required')

    teams = Team.select().where(Team.league_id == league_id)
    serialized = [{
       'id': team.id,
       'name': team.name,
       'short_name': team.short_name,
       'past_n_games': past_n_games,
       'winrate': team.winrate_for_previous_games(past_n_games)
       } for team in teams]

    return json.dumps(serialized)
