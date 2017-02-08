"""
All the logic for creating the app flask instance
"""

from flask import Flask


def create_app():
    """
    Creates the flask app to be used wherever necessary. Pulling this out to another file
    makes it a little easier to tell what's happening in server.py in case this gets more
    complicated over time. In that case, config can be passed as an argument and code can
    be added that overwrites defaults.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
