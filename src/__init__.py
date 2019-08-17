from flask import Flask

from . import db
from src.endpoints import schedule


app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'hello'


db.init_app(app)
app.register_blueprint(schedule.bp)
