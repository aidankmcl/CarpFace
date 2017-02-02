"""This script takes in parsed email data and analyzes it, looking for
specific terms which might identify what an email is about and organizing
emails based on the use of those terms."""

import json
from pprint import pprint

with open('parsed_data/january-2017.json') as data_file:    
    data = json.load(data_file)

pprint(data)