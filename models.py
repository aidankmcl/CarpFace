
from datetime import datetime
import json
import os
import re

from flask_sqlalchemy import SQLAlchemy

from factory import create_app
from email_purpose import food_words, event_words, music_words, item_words, job_words, other_words

db = SQLAlchemy()
# Characters we don't want in our message ids
DEL_CHARS = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
DATE_FORMATS = ['%a %b %d %X %Y', '%a, %d %b %Y %X', '%d %b %Y %X']
TOPIC_DICT = {
    "food": food_words,
    "event": event_words,
    "music": music_words,
    "item": item_words,
    "job": job_words,
    "other": other_words
}


class Email(db.Model):
    """
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
    """

    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(255))
    text = db.Column(db.Text)
    subject = db.Column(db.Text)
    date = db.Column(db.DateTime)
    author_email = db.Column(db.String(255))
    author_name = db.Column(db.String(255))
    replying_to = db.Column(db.String(255))
    tags = db.Column(db.String(100))

    def __init__(self, message_id, text, subject, date, author_email, author_name, replying_to=False, tags=""):
        self.message_id = message_id
        self.text = text
        self.subject = subject
        self.date = date
        self.author_email = author_email
        self.author_name = author_name
        self.replying_to = replying_to if replying_to else ''
        self.tags = tags

    def __repr__(self):
        return '<Email %s>' % (self.subject)

    @property
    def serialized(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "message_id": self.message_id,
            "text": self.text,
            "subject": self.subject,
            "date": self.date.__str__(),
            "author_name": self.author_email,
            "author_email": self.author_name,
            "replying_to": self.replying_to,
            "tags": self.tags
        }


def read_emails(fpath):
    with open(os.path.join(os.path.dirname(__file__), 'parsed_data/', fpath), 'r') as emails:
        return json.loads(emails.read())


def get_date_format(date_string):
    for time_format in DATE_FORMATS:
        try:
            return datetime.strptime(date_string, time_format)
        except:
            pass


def get_email_model(email_json):
    return Email(message_id=email_json["id"],
        text=email_json["text"],
        subject=email_json["subject"],
        date=get_date_format(re.split('\s\-|\s\+', email_json["date"])[0]),
        author_email=email_json["author_email"],
        author_name=email_json["author_name"],
        replying_to=email_json["replying_to"])


def add_emails():
    for email_chunk in os.listdir(os.path.join(os.path.dirname(__file__), 'parsed_data/')):
        emails = [get_email_model(email) for email in read_emails(email_chunk)]
        db.session.bulk_save_objects(emails)
        db.session.commit()


def add_tags(emails):
    for email in emails:
        topic_tags = [topic for topic in TOPIC_DICT for tag in TOPIC_DICT[topic] if email.subject.find(tag) > -1]
        email.tags = ','.join(topic_tags)


if __name__ == "__main__":
    app = create_app()
    db.init_app(app)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #     add_emails()
    #     add_tags(emails)
    #     db.session.commit()
