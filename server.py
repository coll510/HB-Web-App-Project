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
    # date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
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

    # Iterate through events
    #   For every event, pick out the fields you care about from the response
    #   Specifically for time, convert it from the EventBrite format to whatever format you want
    # Pass these new event data into your template

    # add logic here to convert to new format. make adjustments to jinja to reflect it as well.

    # for event in events:
    #     return


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
    return redirect("/login")


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
    return redirect("/user-profile")
    #return redirect("/danceclass-search")

@app.route('/user-profile')
def show_profile():
    """Show user profile info."""

    return render_template("user_info.html")

@app.route('/logout')
def logout():
    """Log out."""
    #add a logout button
    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/saved-classes', methods=['POST'])
def save_class():
    """ Save this class to the database and to the user's list of saved classes."""

    #Get the user id from the session
    #user_id = session["user_id"]
    email= session['user']
    user_id = User.query.filter_by(email=email).one().user_id

    class_name = request.form.get("class_name")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    url = request.form.get("url")
    #how does this specify which table to add to
    #This adds the class info to the database. Still need to make sure it 
    #saves to that users saved classes list.
    class_info = Class(class_name=class_name, start_time=start_time, end_time=
        end_time, url=url)

    db.session.add(class_info)
    db.session.commit()
    # sql = """
    #     INSERT INTO dancers2 (class_name, 
    #     start_time, end_time, url)
    #     VALUES (:class_name, :start_time, :end_time, :url)
    #     """
    # db.session.execute(
    #     sql, { 
    #         "class_name": class_name,
    #         "start_time": start_time,
    #         "end_time": end_time, 
    #         "url": url

    #     }
    # )

    # db.session.add(user_classes)
    # db.session.commit()

    flash("You have successfully saved this class to your profile.")

    return redirect("/search-results")

@app.route('/saved-classes', methods=['GET'])
def my_saved_classes():
    """Query database to find and display the classes a user has saved."""

    user_id = session["user_id"]
#     
   
    #saved = #put sqlalchemy here if i choose to
    #write query for only the logged in user here, not everyone

    # #this query specifies the search by user id
    # saved_query = """
    #       SELECT users.user_id, classes.class_name, classes.url, 
    #       classes.start_time, classes.end_time
    #       FROM classes
    #       JOIN user_classes USING (class_id)
    #       JOIN users on (user_classes.user_id = users.user_id)
    #       WHERE user_classes.class_saved IS True;;
    #       """
    #     #get information on classes saved based on the user id
    # db_cursor = db.session.execute(saved_query, {put html id info here. should match variables
    # i will set in this route above the saved query block.} )

    # db_cursor.fetchall()


    return render_template("classes_saved.html", class_name=class_name, 
    class_url=class_url, start_time=start_time, end_time=end_time) # dancers2=dancers2)

#two routes - 1 to display what the user has already saved and one to post the
#display 




@app.route('/tracked-classes')
def classes_attended():
#     """Query database to find the saved classes that a user has attended."""

#     saved_query = """
#         SELECT classes.class_name, classes.start_time,
#         classes.end_time, classes.url
#         FROM classes
#         JOIN user_classes USING (class_id)
#         WHERE user_classes.class_saved IS True 
#         AND user_classes.class_attended IS True;
#         """
    # db_cursor = db.session.execute(saved_query, {user_classes.user_id = 
      #   users.user_id} )

    # attended_query = """
    #     SELECT * FROM classes
    #     JOIN user_classes USING (class_id)
    #     WHERE class_saved IS True AND class_attended IS TRUE;
    #     """


    return render_template("classes_attended.html")




if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    #Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host="0.0.0.0")