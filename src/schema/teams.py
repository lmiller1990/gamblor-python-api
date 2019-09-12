from peewee import *
from functools import reduce

from .base import BaseModel
from src.models.mappings import map_market_short_to_long_with_id
from src.utils.datetime import stringify_date


class Team(BaseModel):
    from .league import League
    id = PrimaryKeyField()
    name = TextField()
    short_name = TextField()
    league_id = IntegerField()
    league = ForeignKeyField(League, backref='teams')

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

    def last_n_played_games(self, n):
        """
        Return last completed n games for a team

        Params:
            n (int): number of games to consider

        Returns:
            games (src.schema.Game[]): list of games
        """
        from .game import Game
        return self.played_games().order_by(Game.date.desc()).limit(n)

    def to_json(self):
        return {
                'id': self.id,
                'name': self.name,
                'short_name': self.short_name,
                }

    def winrate_for_previous_games(self, n):
        """
        Return the win % over the last n games

        Parameters:
            n: The number of games

        Returns:
            winrate (float): a number between 0 and 1 reflecting win rate
        """

        from .game import Game
        games = self.played_games().order_by(Game.date.desc()).limit(n)
        wins = reduce(lambda acc, curr: acc + 1 if curr.winner_id == self.id else acc, games, 0)
        return wins / len(games)

    def results_for_previous_games(self, n):
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
            opponent_id = game.red_side_team_id if game.blue_side_team_id == self.id else game.blue_side_team_id
            return {
                    'game_id': game.id,
                    'game_number': game.game_number,
                    'date': stringify_date(game.date),
                    'team_id': self.id,
                    'opponent_id': opponent_id,
                    'fb': game.first_blood_team_id == self.id,
                    'ft': game.first_turret_team_id == self.id,
                    'fd': game.first_dragon_team_id == self.id,
                    'fbaron': game.first_baron_team_id == self.id,
                    'win': game.winner_id == self.id
                    }

        return list(map(serialize, games))

    def market_success_over_games(self, games, market):
        """
        Returns % success of a team at given market given a set of games (between 0 and 1)

        Parameters:
            games: A list of schema.Game
            market: 'fb' | 'ft' | 'fd' | 'fbaron'

        Returns:
            success (float): value between 0 and 1
        """
        attr = map_market_short_to_long_with_id(market)
        success = reduce(lambda acc, game: acc + 1 if getattr(game, attr) == self.id else acc, games, 0)
        return (success / len(games))
