from peewee import *

from .base import BaseModel


class League(BaseModel):

    id = PrimaryKeyField()
    name = TextField()
    active = BooleanField(default=False)

    class Meta:
        table_name = 'leagues'
    
    @classmethod
    def find_by_name(cls, name):
        return cls.select().where(cls.name == name).first()

    @classmethod
    def active_leagues(cls):
        return cls.select().where(cls.active)

    def current_split(self):
        from .split import Split

        return (Split
                .select()
                .where(Split.league_id == self.id)
                .order_by(Split.created_at.desc())
                .first())

    def to_json(self):
        return {
                'id': self.id,
                'active': self.active,
                'name': self.name
                }
