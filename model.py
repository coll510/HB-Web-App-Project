
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

""" Model Definitions """

class User(db.Model):
    """User"""

    __tablename__ = "users"


    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(60), nullable = False, unique=True)
    email = db.Column(db.String(60), nullable = False, unique=True)

    def __repr__(self):
        return "<User id = {user_id} name = {name} email = {email}>".format(
            user_id=self.user_id, name=self.name, email=self.email)

class Class(db.Model):
    """Class"""

    __tablename__ = "classes"


    class_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False, unique=True)
    

    def __repr__(self):
        return "<Class id = {class_id} name = {name}>".format(
            user_id=self.user_id, name=self.name)


class UserClass(db.Model):
    """User Class"""

    __tablename__ = "userClasses"


    userClass_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id") 
                        nullable = False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.class_id")
                            nullable = False)
    class_saved = db.Column(db.String(100))
    class_attended = db.Column(db.String(100))

    #human = db.relationship("Human", backref="humans") Put backrefs here?

    def __repr__(self):
        return "<User class id = {userClass_id} user id = {user_id} class id = {class_id} class_saved = {class_saved} class_attended = {class_attended}>".format(
            userClass_id=self.userClass_id, user_id=self.user_id, class_id=self.class_id, 
            class_saved = self.class_saved, class_attended = self.class_attended)       