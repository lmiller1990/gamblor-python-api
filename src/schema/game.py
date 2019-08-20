from datetime import datetime
from peewee import *

from .base import BaseModel
from src.utils.datetime import stringify_date


class Game(BaseModel):
    from .teams import Team
    from .split import Split
    from .league import League

    id = PrimaryKeyField()
    red_side_team = ForeignKeyField(Team, column_name='red_side_team_id')
    blue_side_team = ForeignKeyField(Team, column_name='blue_side_team_id')
    winner = ForeignKeyField(Team, backref='won_games', column_name='winner_id')
    winner_id = IntegerField(Team)
    loser = ForeignKeyField(Team, backref='lost_games', column_name='loser_id')
    loser_id = IntegerField(Team)

    red_side_team_id = IntegerField(Team)
    blue_side_team_id = IntegerField(Team)
    first_blood_team_id = IntegerField(Team)
    first_turret_team_id = IntegerField(Team)
    first_dragon_team_id = IntegerField(Team)
    first_baron_team_id = IntegerField(Team)

    blue_side_team_fb_odds = DoubleField()
    blue_side_team_fd_odds = DoubleField()
    blue_side_team_ft_odds = DoubleField()
    blue_side_team_fbaron_odds = DoubleField()

    red_side_team_fb_odds = DoubleField()
    red_side_team_fd_odds = DoubleField()
    red_side_team_ft_odds = DoubleField()
    red_side_team_fbaron_odds = DoubleField()

    date = DateTimeField()
    split = ForeignKeyField(Split, backref='games')
    league = ForeignKeyField(League)

    class Meta:
        table_name = 'games'

    def to_json(self):
        return {
                'id': self.id,
                'date': self.date,
                'split_id': self.split.id,
                'league_id': self.league.id,
                'date': stringify_date(self.date),
                'blue_side_team_id': self.blue_side_team_id,
                'red_side_team_id': self.red_side_team_id,
                'winner_id': self.winner_id,
                'loser_id': self.loser_id,
                'blue_side_team_fb_odds': self.blue_side_team_fb_odds,
                'blue_side_team_ft_odds': self.blue_side_team_ft_odds,
                'blue_side_team_fd_odds': self.blue_side_team_fd_odds,
                'blue_side_team_fbaron_odds': self.blue_side_team_fbaron_odds,
                'red_side_team_fb_odds': self.red_side_team_fb_odds,
                'red_side_team_ft_odds': self.red_side_team_ft_odds,
                'red_side_team_fd_odds': self.red_side_team_fd_odds,
                'red_side_team_fbaron_odds': self.red_side_team_fbaron_odds
                }

    @classmethod
    def previous_n_regular_season_games_for_team(cls, team, n, game_date):
        games =  [
                g for g in (cls
                    .select()
                    .where(
                        (
                            (cls.blue_side_team_id == team.id) |
                            (cls.red_side_team_id == team.id)
                        ) &
                        (
                            Game.date < game_date
                        ) &
                        (
                            (
                                (Game.date > datetime(2019, 1, 1))
                                # remove to exclude playoff games from prev. split
                                & (Game.date < datetime(2019, 3, 30))
                            ) |
                            (
                                (Game.date > datetime(2019, 6, 1)) &
                                (Game.date < datetime(2019, 8, 8))
                            )
                        )
                    )
                    .limit(n)
                    .order_by(cls.date.desc())
                    )
                ]

        games.reverse()
        return games

    @classmethod
    def played_by_team_before_date(cls, team, game_date, n=15):
        return team.played_games().where(cls.date < game_date).limit(n).order_by(cls.date.desc())
