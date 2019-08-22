from flask import Flask
from flask_cors import CORS

from . import db
from src.endpoints import schedule
from src.endpoints import leagues
from src.endpoints import previous_game_results
from src.endpoints import recommendations
from src.endpoints import splits
from src.endpoints import teams


app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello():
    return 'hello'


db.init_app(app)
app.register_blueprint(schedule.bp)
app.register_blueprint(leagues.bp)
app.register_blueprint(previous_game_results.bp)
app.register_blueprint(recommendations.bp)
app.register_blueprint(splits.bp)
app.register_blueprint(teams.bp)
