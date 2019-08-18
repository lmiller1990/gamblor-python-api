from peewee import *

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
