from peewee import *

from .base import BaseModel


class League(BaseModel):

    id = PrimaryKeyField()
    name = TextField()

    class Meta:
        table_name = 'leagues'
    
    @classmethod
    def find_by_name(cls, name):
        return cls.select().where(cls.name == name).first()

    def current_split(self):
        from .split import Split

        return (Split
                .select()
                .where(Split.league_id == self.id)
                .order_by(Split.created_at.desc())
                .first())
