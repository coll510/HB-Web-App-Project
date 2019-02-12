from pprint import pformat
import os
#os is python's os module
#pretty print and pretty format

import requests
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
# app.secret_key = "secretsecretsecret" 
# #This pulls from my os so connect this to my secrets.sh file.

# EVENTBRITE_TOKEN = os.environ.get('#')
# #put variable name of my secrets file token

# EVENTBRITE_URL = 
# #get url from eventbrite
# USER_ID = 
#my eventbrite user id

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


















if __name__ == "__main__":
    app.debug = True

    #connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")