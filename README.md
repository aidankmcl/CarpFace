# CarpFace
Data visualization for the carpediem email list at Olin

## Installing

To install, start with `pip install -r requirements.txt` ([virtual environment](https://virtualenv.pypa.io/en/stable/) recommended).
In order to see any data, you'll need an Olin email and a subscription to the CarpeDiem mailing list. Once you've signed up, follow the instructions in the `scrape.js` file:
```
To use, install casperjs (npm install -g casperjs) and run:
casperjs scrape.js <arg1> <arg2>
where arg1 is your email for carpe and arg2 is your password for carpe.

If you don't think you have a password for carpe, you do but it's randomly
generated. You'll need to visit the carpediem list at lists.olin.edu to
get it reset.
```

After that, run `python wrangle.py` which will do a rough parse of all the scraped data and make it accessible to the web app. Then you're ready to go! Just run `python server.py` and visit `localhost:5000`.

## More Info

### Vision

This repo is intended to provide a frontend for any of the mailing list data dumps at Olin college. The hope is to have something accessible enough that any student familiar with the command line could hop in and explore historical email data.

### What does the software do?

Right now, the software provides both topic and date range filters on top of carpediem historical data so that anybody who completes the setup can sift through all data up until the point of scrape. Unless the data format changes, these scripts should be able to interpret future data thus the project has no set time limitations.

The project currently looks like the following:

* Overall
![Overall](/screenshots/total.png)

* Topic filtering
![Topic Filtering](/screenshots/filter.png)

* Date filtering
![Date Filtering](/screenshots/date.png)


### How does the code work?

The bulk of the logic revolves around scraping email data and getting it into a usable format, in this case a SQLite database being accessed using flask-sqlalchemy.

This is broken down into three bits:
* `scrape.js` uses casperjs to get all of the raw data
* `wrangle.py` puts that raw data into clean JSON with relevant fields
* `models.py` has logic for taking the JSON generated by `wrangle.py` and inserting it into a SQLite database.

Finally `server.py` has fairly generic code for serving pages, but most importantly an endpoint for sending filter information (date range, topics) and getting back a set of emails that fit the selected criteria.

Presently this repository assumes Python 2.7, but might work in Python3 since there's only one print statement and it has parenthesis :)

### Issues and enhancements

Right now the primary issue is that the data is not super clean and there are certainly instances when the wrong pieces of email are selected for the text (or more than one email is globbed into one). Although this is relatively rare, amongst >32,000 emails at the time of writing I'd imagine even a small error percentage translates into a fair amount of bunk data.

A pleasant enhancement would be a more usable and attractive frontend - the current one works but for an app focused on making sifting a nice experience, it's not particularly clean.

Another cool direction would be analysis of the data to see long term trends. What do these emails say about student life at Olin? Spooky!
