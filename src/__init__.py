from flask import Flask

from . import db
from src.endpoints import schedule
from src.endpoints import leagues
from src.endpoints import splits


app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'hello'


db.init_app(app)
app.register_blueprint(schedule.bp)
app.register_blueprint(leagues.bp)
app.register_blueprint(splits.bp)
