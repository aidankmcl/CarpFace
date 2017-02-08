from datetime import datetime
import json
import os
import re

from flask_sqlalchemy import SQLAlchemy

from factory import create_app

db = SQLAlchemy()
# Characters we don't want in our message ids
DEL_CHARS = ''.join(c for c in map(chr, range(256)) if not c.isalnum())


class Email(db.Model):
    '''
    Parser returns:
    {
        "id":           id assigned by carpediem mail server,
        "text":         raw email text (includes newlines, etc.),
        "subject":      email subject,
        "date":         send date,
        "author_name":  sender name,
        "author_email": sender email,
        "replying_to":  if a reply, the ID of the email being replied to
    }
    '''
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(255))
    text = db.Column(db.Text)
    subject = db.Column(db.Text)
    date = db.Column(db.DateTime)
    author_email = db.Column(db.String(255))
    author_name = db.Column(db.String(255))
    replying_to = db.Column(db.String(255))

    def __init__(self, message_id, text, subject, date, author_email, author_name, replying_to=False):
        self.message_num = message_id
        self.text = text
        self.subject = subject
        self.date = date
        self.author_email = author_email
        self.author_name = author_name
        self.replying_to = replying_to if replying_to else ''

    def __repr__(self):
        return '<Email %s>' % (self.subject)


def read_emails(fpath):
    with open(os.path.join(os.path.dirname(__file__), 'parsed_data/', fpath), 'r') as emails:
        return json.loads(emails.read())


def get_email_model(email_json):
    try:
        time = datetime.strptime(email_json["date"].replace(',', ''), '%a %b %d %X %Y')
    except ValueError as exception:
        # Inconsistent date format...
        print re.split('\-|\+', email_json["date"])
        time = datetime.strptime(re.split('\s\-|\s\+', email_json["date"])[0], '%a, %d %b %Y %X')
    return Email(message_id=email_json["id"],
        text=email_json["text"],
        subject=email_json["subject"],
        date=time,
        author_email=email_json["author_email"],
        author_name=email_json["author_name"],
        replying_to=email_json["replying_to"])


def add_emails():
    for email_chunk in os.listdir(os.path.join(os.path.dirname(__file__), 'parsed_data/')):
        print email_chunk
        emails = [get_email_model(email) for email in read_emails(email_chunk)]
        db.session.bulk_save_objects(emails)
        db.session.commit()

if __name__ == "__main__":
    app = create_app()
    db.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()
        add_emails()
