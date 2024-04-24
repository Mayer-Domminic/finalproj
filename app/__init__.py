from flask import Flask
from psycopg import connect
from . import views

def create_app():
    app = Flask(__name__)
    # add postgres to flask
    app.config['DATABASE_URI'] = 'postgres://postgres:abc123@localhost:5432/workout'

    # open the postgres db
    @app.before_first_request
    def initialize_database():
        app.db = connect(app.config['DATABASE_URI'])
    # register views.py for blueprinting
    app.register_blueprint(views.bp)

    return app