"""This script takes in parsed email data and analyzes it, looking for
specific terms which might identify what an email is about and organizing
emails based on the use of those terms."""

import json
from pprint import pprint


food_words = ['pizza', 'protein', 'wave', 'food', 'fireside', 'bar']
event_words = ['march', 'transportation', 'jan', 'february', '2017', '2017-18', 'share', 'contest', 'conference', 'sing-along', 'thursdays', 'livestream', 'happening', 'begins', 'slac']
music_words = ['concert', 'sing-along']
item_words = ['matches', 'sale', 'stuff', 'blocks', 'free', 'ticket', 'dell', 'class', 'selling', 'buy', 'spreadsheet', 'tickets']
job_words = ['hiring', 'job', 'research']
other_words = ['strava', 'archers', 'survey', 'self-defense', 'club']

food_emails = {}
event_emails = {}
music_emails = {}
item_emails = {}
job_emails = {}
other_emails = {}


if __name__ == "__main__":
    with open('parsed_data/january-2017.json') as data_file:    
        data = json.load(data_file)

    for val in range(len(data)):
        subject = data[val]['subject']
        new_subject = subject.split()
        new_subject.remove('[Carpediem]')
        for word in new_subject:
            word = word.lower()
            if word in food_words:
                food_emails['email%s' %val] = new_subject
            elif word in event_words:
                event_emails['email%s' %val] = new_subject
            elif word in music_words:
                music_emails['email%s' %val] = new_subject
            elif word in item_words:
                item_emails['email%s' %val] = new_subject
            elif word in job_words:
                job_emails['email%s' %val] = new_subject
            elif word in other_words:
                other_emails['email%s' %val] = new_subject

    print food_emails
