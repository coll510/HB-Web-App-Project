
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

""" Model Definitions """

class User(db.Model):
    """User"""

    __tablename__ = "users"


    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(60), nullable = False, unique=True)
    email = db.Column(db.String(60), nullable = False, unique=True)

    # def __repr__(self):
    #     return "<User id = {user_id} name = {user_name} email = {email}>".format(
    #         user_id=self.user_id, name=self.user_name, email=self.email)

    def __repr__(self):
        """Provide helpful information when printed."""

        return f"<User user_id={self.user_id} user_name={self.user_name} email={self.email}>"

class Class(db.Model):
    """Class"""

    __tablename__ = "classes"


    class_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    class_name = db.Column(db.String(100), nullable = False, unique=True)
    

    # def __repr__(self):
    #     return "<Class id = {class_id} name = {class_name}>".format(
    #         user_id=self.user_id, name=self.class_name)
    def __repr__(self):
        """Provide helpful information when printed."""

        return f"<Class class_id={self.class_id} class_name={self.class_name}>"


class UserClass(db.Model):
    """User Class"""

    __tablename__ = "user_classes"


    user_class_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable = False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.class_id"),
                            nullable = False)
    class_saved = db.Column(db.String(100))
    class_attended = db.Column(db.String(100))

    user = db.relationship("User", backref="user_classes") 

    # def __repr__(self):
    #     return "<UserClass class id = {userClass_id} user id = {user_id} class id = {class_id} class_saved = {class_saved} class_attended = {class_attended}>".format(
    #         userClass_id=self.userClass_id, user_id=self.user_id, class_id=self.class_id, 
    #         class_saved = self.class_saved, class_attended = self.class_attended) 
    def __repr__(self):
        """Provide helpful information when printed."""

        return f"<UserClass user_class_id={self.user_class_id} user_id={self.user_id} class_id={self.class_id} class_saved={self.class_saved} class_attended={self.class_attended}>"    


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dancers'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")  