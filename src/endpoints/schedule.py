from flask import Blueprint, request
import json


from src.schema.league import League


bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def schedule():
    """
    Return upcoming games for a given league

    Parameters:
        league: the name thee league

    Example:
        curl /schedule?league=NA_LCS_2019

    Example response:
        {
            "games": [
                {
                    "blue_side_team_fb_odds" : 2.1,
                    "blue_side_team_fbaron_odds" : 2.62,
                    "blue_side_team_fd_odds" : 2.2,
                    "blue_side_team_ft_odds" : 2.25,
                    "blue_side_team_id" : 119,
                    "date" : "2019-08-22 00:00:00",
                    "id" : 1077,
                    "league_id" : 2,
                    "loser_id" : null,
                    "red_side_team_fb_odds" : 1.66,
                    "red_side_team_fbaron_odds" : 1.44,
                    "red_side_team_fd_odds" : 1.61,
                    "red_side_team_ft_odds" : 1.57,
                    "red_side_team_id" : 4,
                    "split_id" : 4,
                    "winner_id" : null
                }
            ],
            "league_id" 2
        }
    """
    name = request.args.get('league').replace('_', ' ')
    league = League.find_by_name(name)
    split = league.current_split()
    unplayed_games = split.unplayed_games()

    return json.dumps({
        'league_id': league.id,
        'games': [g.to_json() for g in unplayed_games]
        }, default=str)
