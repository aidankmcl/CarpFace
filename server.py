"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""

import os
import json
import re
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import or_, and_

from factory import create_app
from models import db, Email

from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

app = create_app()
db.init_app(app)


@app.route('/health')
def health():
    return 'ok'


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n')) for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route('/')
def home_page():
    dates = sorted(set(map(lambda fname: re.findall('\d+', fname)[0], os.listdir('parsed_data'))))
    return render_template('index.html', dates=dates)


@app.route('/email/<id>')
def single_email_view(id):
    email = Email.query.filter_by(message_id=id).first()
    return render_template('single.html', email=email)


@app.route('/emails', methods=["POST"])
def filter_emails():
    topic_filters = list(request.form.get("topics", "").split(','))  # explicit conversion to list in case there's only one tag
    dates = request.form.get("date_range", "01/01/2005 - 01/31/2005").split(" - ")  # sets default to Jan 2005
    start_date, end_date = datetime.strptime(dates[0], '%m/%d/%Y'), datetime.strptime(dates[1], '%m/%d/%Y')
    emails = Email.query.filter(and_(Email.date.between(start_date, end_date), or_(Email.tags.contains(tag) for tag in topic_filters))).all()
    return json.dumps([e.serialized for e in emails])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    app.run(host=host, debug=True, port=port)
