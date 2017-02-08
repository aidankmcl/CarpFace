"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""

import os
import json
import re

from flask import Flask, redirect, render_template, request, url_for

from factory import create_app
from models import db

app = create_app()
db.init_app(app)


@app.route('/health')
def health():
    return 'ok'


@app.route('/')
def home_page():
    dates = sorted(set(map(lambda fname: re.findall('\d+', fname)[0], os.listdir('parsed_data'))))
    return render_template('index.html', dates=dates)


@app.route('/data/<month_year>')
def data_query(month_year):
    try:
        with open(os.path.join("parsed_data/", month_year + ".json"), "r") as json_text:
            data = json_text.read()
    except IOError as e:
        data = json.dumps([])
        print e
    return data


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    app.run(host=host, debug=True, port=port)
