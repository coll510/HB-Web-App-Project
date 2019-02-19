from pprint import pprint
import os
#os is python's os module
#pretty print and pretty format

import requests
from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
#import ipdb 
from datetime import datetime
from model import connect_to_db, db, User, Class, UserClass


app = Flask(__name__)
app.secret_key = "secretsecretsecret" 
# #This pulls from my os so connect this to my secrets.sh file.

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"
USER_ID = os.environ.get('EVENTBRITE_USER_ID')
AUTH_HEADER = {"token": EVENTBRITE_TOKEN}



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
    if distance:
        distance = distance + "mi"
    time = request.args.get("time")

    # date_time_str = '2019-02-24T09:00:00' 
    # date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    # #imported datetime and started process to convert api date to human readable
    #format
    #perhaps get start.date.range and end date range from api and then pass those
    #variables into the date time obj
    #check eventrite lab for more info
    
        #yellow - api params to get
    if location and style and distance:
        # search by dance style, location and distance  
        payload = {"q": f"dance class {style}", 
                    "location.address": location,
                    "location.within" : distance,
                    "sort_by": sort, 
                    "start_date.keyword": time,
                    "token": EVENTBRITE_TOKEN}
        

    elif location and style:
        # search by dance style and location 
        payload = {"q": f"dance class {style}", 
                    "location.address": location,
                    "sort_by": sort, 
                    "start_date.keyword": time,
                    "token": EVENTBRITE_TOKEN}
    
    elif location and distance:
 
        #search any dance class by location and distance
        payload = {"q": "dance class", 
                    "location.address" : location, 
                    "location.within" : distance,
                    "sort_by" : sort,
                    "start_date.keyword": time,
                    "token": EVENTBRITE_TOKEN}

    
    else:
        #general query search of "dance class" by location
        payload = {"q": "dance class",
                    "location.address": location,
                    "sort_by": sort,
                    "start_date.keyword": time,
                    "token": EVENTBRITE_TOKEN}


    response = requests.get("https://www.eventbriteapi.com/v3/events/search/", params=payload) 
                           
    print("search url")   
    print(response.url)


    data = response.json()
    events = data['events'] 
    pprint(data)
    #import pdb; pdb.set_trace()

    #Redirect to search page if results are empty.
    if response.ok and events == []:
        flash("Your search result didn't return any classes. Please search again.")
        return redirect("/danceclass-search")

    #Return results
    elif response.ok:
        classes = data['events']
       

    else: 
        flash(f"No classes: {data['error_description']}")
    #     classes = []
    # need to add an elif/else statement for if there are no result


    return render_template("/search-results.html", 
                            events=events)
   
  

    

    # else: 
    #     flash("Please complete the required information.")
    #     return redirect("/danceclass-search")


@app.route('/register', methods = ['GET'])
def registration_form():
    """Show registration form to user to sign up to access more features."""

    return render_template("registration_form.html")

@app.route('/register', methods = ['POST'])
def complete_registration():
    """Process user's registration to app"""

    #get form variables and add user to database

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(user_name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"Welcome {name}. Add catchphrase or something.")
    return redirect("/danceclass-search")

@app.route('/login', methods = ['GET'])
def login_form():
    """Show login form to user."""

    return render_template("login_form.html")

@app.route('/login', methods = ['POST'])
def complete_login():
    """Log user in."""

    #Get variables from form and log user in to app.

    email = request.form["email"]
    password = request.form["password"]
    #find the user in the database
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Please register to be able to login.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("danceclass-search")

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")















if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    #Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")