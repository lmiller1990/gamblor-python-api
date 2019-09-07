from flask import g
from peewee import *
import os


def get_db():
    if 'db' not in g:
        g.db = PostgresqlDatabase(
          os.environ['POSTGRES_DB'],
          user=os.environ['POSTGRES_USER'],
          host=os.environ['POSTGRES_HOST'],
          password=os.environ['POSTGRES_PASS'],
        )
        g.db.connect()

    return g.db


def close_db(e=None):
    db = get_connection()

    if db is not None:
        db.close()


_connection = None


def get_connection():
    global _connection
    if not _connection:
        db = PostgresqlDatabase(
                os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                host=os.environ['POSTGRES_HOST'],
                password=os.environ['POSTGRES_PASS'],
                # sslmode=os.environ['SSLMODE']
                )
        db.connect()
        _connection = db

    return _connection


def init_app(app):
    app.teardown_appcontext(close_db)
