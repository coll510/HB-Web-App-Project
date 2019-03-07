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
    
    #yellow/city is the name in my html file
    distance = request.args.get("distance")
    sort = request.args.get("sort")
    style = request.args.get("style")
    if distance:
        distance = distance + "mi"
    time = request.args.get("time")


    
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
    


    data = response.json()
    events = data['events'] 


    processed_events = []
    for event in events: 
        name = event['name']['text']
        start_time = get_readable_date(event['start']['local'])
        end_time = get_readable_date(event['end']['local'])
        url = event['url']

        processed_event = {
            'name': name,
            'start_time': start_time,
            'end_time': end_time,
            'url': url
        }

        processed_events.append(processed_event)

   


    #pprint(data)
    #import pdb; pdb.set_trace()

    # if response.ok:
    #     events = data.json()['events']
    #     if events == []:
    #         # whatever
    #     else:
    #         # do the good stuff

    #Redirect to search page if results are empty.
    if response.ok and events == []:
        flash("Your search result didn't return any classes. Please search again.")
        return redirect("/danceclass-search")

    #Return results
    elif response.ok:
        events = data['events']
       

    else: 
        flash(f"No classes: {data['error_description']}")
        return redirect("/danceclass-search")
    


    return render_template("/search-results.html", 
                            events=processed_events)
    
    # else: 
    #     flash("Please complete the required information.")
    #     return redirect("/danceclass-search")

def get_readable_date(iso_formatted_string):

    date_time_obj = datetime.strptime(iso_formatted_string, '%Y-%m-%dT%H:%M:%S')
   
    return date_time_obj.strftime('%m/%d/%Y Time: %I:%M %p')
    

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

    user_id = session["user_id"]

    attended = UserClass.query.filter(UserClass.user_id==user_id, UserClass.class_attended==True).all()

    
    jan = sum(user_class.dance_class.start_time.month == 1 for user_class in attended)
    feb = (user_class.dance_class.start_time.strftime('%m') == "02" for user_class in attended)
    mar = sum(user_class.dance_class.start_time.strftime('%m') == "03" for user_class in attended)
    apr = sum(user_class.dance_class.start_time.strftime('%m') == "04" for user_class in attended)
    may = sum(user_class.dance_class.start_time.strftime('%m') == "05" for user_class in attended)
    jun = sum(user_class.dance_class.start_time.strftime('%m') == "06" for user_class in attended)
    jul = sum(user_class.dance_class.start_time.strftime('%m') == "07" for user_class in attended)
    aug = sum(user_class.dance_class.start_time.strftime('%m') == "08" for user_class in attended)
    sep = sum(user_class.dance_class.start_time.strftime('%m') == "09" for user_class in attended)
    octo = sum(user_class.dance_class.start_time.strftime('%m') == "10" for user_class in attended)
    nov = sum(user_class.dance_class.start_time.strftime('%m') == "11" for user_class in attended)
    dec = sum(user_class.dance_class.start_time.strftime('%m') == "12" for user_class in attended)
    
    # try:
    #     #try to make january/each month a variable with a sum. if nothing is there, then make it 0



    # except:
    # #put the error here that I get if it doesn't exist. may be a type error. set it to 0.

    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec]

    return render_template("user_info.html", months=months)

@app.route('/logout')
def logout():
    """Log out."""
    #add a logout button on the top of the pages in base.html.
    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/saved-classes', methods=['POST'])
def save_class():
    """ Save this class to the database and to the user's list of saved classes."""
    
    #Get the user id from the session
    user_id = session["user_id"]


    
       #save class info to database table class
    class_name = request.form.get("class_name")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    url = request.form.get("url")
    print(class_name)
    start_time = datetime.strptime(start_time.strip(), '%m/%d/%Y Time: %I:%M %p')
    end_time = datetime.strptime(end_time.strip(), '%m/%d/%Y Time: %I:%M %p')
    

    existing_class = Class.query.filter_by(class_name=class_name).first() 
    #Class queries for the whole class object. 
    if not existing_class:

    
    #This adds the class info to the database. 
        class_info = Class(class_name=class_name, start_time=start_time, 
                       end_time=end_time, url=url)

        db.session.add(class_info)
        db.session.commit()
        class_id = class_info.class_id #this will get the new class id for that class. 
            
    if existing_class:
        class_id = existing_class.class_id

    #Add user_class info to database table user_class

    saved_class = UserClass(user_id=user_id, class_id=class_id, class_saved=True, class_attended=False)

    db.session.add(saved_class)
    db.session.commit()
    
       

    message = "You have successfully saved this class to your profile."

    return(message)
    #return redirect("/search-results")

@app.route('/saved-classes', methods=['GET'])
def my_saved_classes():
    """Query database to find and display the classes a user has saved."""

    user_id = session["user_id"]

    saved_classes = UserClass.query.filter_by(user_id=user_id).all()
    
    users_saved_classes = []
    for user_class in saved_classes: 
        name = user_class.dance_class.class_name 
        start_time = get_saveable_date(user_class.dance_class.start_time)
        end_time = get_saveable_date(user_class.dance_class.end_time)
        url = user_class.dance_class.url

        saved_class = {
            'name': name,
            'start_time': start_time,
            'end_time': end_time,
            'url': url
        }
    
        users_saved_classes.append(saved_class)
        
    return render_template("classes_saved.html", users_saved_classes=users_saved_classes) 


def get_saveable_date(iso_string):


    return iso_string.strftime('%m/%d/%Y Time: %I:%M %p')

@app.route('/tracked-classes', methods=['POST'])
def mark_class_attended():

    user_id = session["user_id"]

    class_names = request.form.getlist("class_name") #added section
    #query the userclass table by user id and class id
    
    #class1 because class is a protected python keyword
    for class1 in class_names:

        class_id = Class.query.filter_by(class_name=class1).first().class_id
        saved_class = UserClass.query.filter_by(class_id=class_id, user_id=user_id).first() #added
        
        #changes the attendance field for this row
        saved_class.class_attended = True

        db.session.commit()
    #return redirect to tracked classes route
    return redirect('/tracked-classes')

@app.route('/tracked-classes', methods=['GET'])
def classes_attended():
#     """Query database to find the saved classes that a user has attended."""
    user_id = session["user_id"]

    attended = UserClass.query.filter_by(user_id=user_id, class_attended=True).all()
    print(attended) 

    user_attended_classes = []
    for user_class in attended: 
        name = user_class.dance_class.class_name 
        start_time = get_saveable_date(user_class.dance_class.start_time)
        end_time = get_saveable_date(user_class.dance_class.end_time)
        url = user_class.dance_class.url

        tracked_class = {
            'name': name,
            'start_time': start_time,
            'end_time': end_time,
            'url': url
        }
    
        user_attended_classes.append(tracked_class)
    

    return render_template("classes_attended.html", user_attended_classes=user_attended_classes) 
    
    # attended_query = """
    #     SELECT * FROM classes
    #     JOIN user_classes USING (class_id)
    #     WHERE class_saved IS True AND class_attended IS TRUE;
    #     """
     
    # db_cursor = db.session.execute(attended_query, {user_classes.user_id = 
      #   users.user_id} )

    


    #return render_template("classes_attended.html")


@app.route("/attended-chart.json")
def classes_attended_data():
    #Show classes attended data in chart.js

    user_id = session["user_id"]

    attended = UserClass.query.filter(UserClass.user_id==user_id, UserClass.class_attended==True).all()

    
#     #jan = sum(user_class.dance_class.start_time.month == 1 for user_class in attended)
#     feb = (user_class.dance_class.start_time.strftime('%m') == "02" for user_class in attended)
    mar = sum(user_class.dance_class.start_time.strftime('%m') == "03" for user_class in attended)
    
    # try:
    #     #try to make january/each month a variable with a sum. if nothing is there, then make it 0



    # except:
    # #put the error here that I get if it doesn't exist. may be a type error. set it to 0.

    # months = [jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec]
               
    return 


        
    

#     return render_template("classes_attended.html", user_attended_classes=user_attended_classes)

#     data_dict = {
#                 "labels": [ 
#                     "January", "February", "March", "April",
#                     "May", "June", "July", "August", 
#                     "September", "October", "November", 
#                     "December"
#                 ],
#                 "datasets": [
#                     {
#                         "data": [4, 9, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         "backgroundColor": [
#                                 'rgba(255, 99, 132, 0.2)',
#                                 'rgba(54, 162, 235, 0.2)',
#                                 'rgba(255, 206, 86, 0.2)',
#                                 'rgba(75, 192, 192, 0.2)',
#                                 'rgba(153, 102, 255, 0.2)',
#                                 'rgba(255, 159, 64, 0.2)',
#                                 'rgba(255, 99, 132, 0.2)',
#                                 'rgba(54, 162, 235, 0.2)',
#                                 'rgba(255, 206, 86, 0.2)',
#                                 'rgba(75, 192, 192, 0.2)',
#                                 'rgba(153, 102, 255, 0.2)',
#                                 'rgba(255, 159, 64, 0.2)'
#                         ] 
#                     }]
#     }

#     return jsonify(data_dict)

#create a statement user attended classes = json.dumps(user attenden clawsses)
    
    #in my html file let user attended classes = JSON.parse({{ user attended classes | tojson}});



if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    #Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host="0.0.0.0")