from peewee import *

from .base import BaseModel

class Team(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    short_name = TextField()

    class Meta:
        table_name = 'teams'

    def games(self):
        """
        Returns all games a team participated in, or will participate in.
        """

        from .game import Game
        return Game.select().where(
                (Game.red_side_team_id == self.id)
                | (Game.blue_side_team_id == self.id))

    def played_games(self):
        """
        Returns all past games a team participated in.
        """

        from .game import Game
        return self.games().where(Game.winner_id != None)

    def results_for_previous_games(self, n=14):
        """
        Return the fb/ft/fd etc for the past n completed games

        Parameters:
            n: the number of previous games to get results for

        Example:
            results = Team.select().first().results_for_previous_games(n=10)
        """

        from .game import Game
        games = self.played_games().order_by(Game.date.desc()).limit(n)

        def serialize(game):
            return {
                    'game_id': game.id,
                    'fb': game.first_blood_team_id == self.id,
                    'ft': game.first_turret_team_id == self.id,
                    'fd': game.first_dragon_team_id == self.id,
                    'fbaron': game.first_baron_team_id == self.id,
                    'win': game.winner_id == self.id
                    }

        return list(map(serialize, games))

    def market_success_over_games(self, games, market):
        mapper = {
                'FBaron': 'first_baron_team_id',
                'FB': 'first_blood_team_id',
                'FD': 'first_dragon_team_id',
                'FT': 'first_turret_team_id'
                }

        success = 0
        for game in games:
            if getattr(game, mapper[market]) == self.id:
                success += 1

        return (success / len(games))

