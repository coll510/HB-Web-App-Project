from pprint import pformat
import os
#os is python's os module
#pretty print and pretty format

import requests
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
#import ipdb 


app = Flask(__name__)
app.secret_key = "secretsecretsecret" 
# #This pulls from my os so connect this to my secrets.sh file.

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
# #put variable name of my secrets file token

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"
# #get url from eventbrite
USER_ID = os.environ.get('EVENTBRITE_USER_ID')
#my eventbrite user id

AUTH_HEADER = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

# i will need to parse the json data that I get from eventbrite's api, set a
#variable or variables that I want to use for the data, and send it to a diff
#html form so that it displays to the user. So practice printing the json 
#data from the balloonicorn server.py file to see an example of how it's
#received, etc. Check lines 61 - 66 of that file.

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")

@app.route("/danceclass-search")
def show_classsearch_form():
    """Show dance class search form."""

    return render_template("danceclass-search.html")

@app.route("/search-results")
def find_danceclasses():
    """Search for and display dance class results from API."""

    #ipdb.set_trace()
    location = request.args.get("city")
    #print(dir(requests))
    #yellow/city is the name in my html file
    distance = request.args.get("distance")
    sort = request.args.get("sort")
    style = request.args.get("style")
    distance = distance + "mi"

    if location and distance:

        #distance = distance 

        payload = {"q": "dance class", 
                    "location.address" : location, 
                    "location.within" : distance,
                    "sort_by" : sort
        #yellow - api params to get

        }

    elif location and style:
        # search by dance style in the query 
        payload = {"q": f"dance class {style}", 
                    "location.address": location,
                    "sort_by": sort

        }

    else:
        #general query search of "dance class"
        payload = {"q": "dance class",
                    "location.address": location,
                    "sort_by": sort 
                    }


    response = requests.get(EVENTBRITE_URL + "events/search", 
                            params = payload, 
                            headers=AUTH_HEADER)

    data = response.json()

    if response.ok:
        classes = data['events']

    else: 
        flash(f"No classes: {data['error_description']}")
        classes = []

    return render_template("/search-results.html", 
                            data=pformat(data),
                            results=classes)

# else: 
#     flash("Please complete the required information.")
#     return redirect("/danceclass-search")


















if __name__ == "__main__":
    app.debug = True

    #connect_to_db(app)

    #Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")