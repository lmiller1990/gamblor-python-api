from peewee import *

from src.utils.datetime import stringify_date
from .base import BaseModel
from .league import League


class Split(BaseModel):

    id = PrimaryKeyField()
    name = TextField()
    league = ForeignKeyField(League)
    created_at = DateTimeField()

    class Meta:
        table_name = 'splits'

    def unplayed_games(self):
        from .game import Game

        return self.games.select().where(Game.winner == None)

    def to_json(self):
        return {
                'id': self.id,
                'name': self.name,
                'league_id': self.league.id,
                'created_at': stringify_date(self.created_at)
                }
