from peewee import *

from src.db import get_connection


class BaseModel(Model):

    class Meta:
        database = get_connection()

