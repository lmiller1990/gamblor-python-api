from flask import Flask

from . import db
from src.endpoints import schedule
from src.endpoints import leagues
from src.endpoints import splits
from src.endpoints import previous_game_results


app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'hello'


db.init_app(app)
app.register_blueprint(schedule.bp)
app.register_blueprint(leagues.bp)
app.register_blueprint(previous_game_results.bp)
app.register_blueprint(splits.bp)
