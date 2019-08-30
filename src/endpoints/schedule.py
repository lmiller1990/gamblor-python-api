from flask import Blueprint, request
import json


from src.schema.league import League


bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def schedule():
    """
    Return upcoming games for a given league

    Parameters:
        league: id of the league to get schedule for

    Example:
        curl /schedule?league=3

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
    league_id = int(request.args.get('league'))
    league = League.get_by_id(league_id)
    split = league.current_split()
    unplayed_games = split.unplayed_games()

    return json.dumps([g.to_json() for g in unplayed_games])
