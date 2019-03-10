
from flask_sqlalchemy import SQLAlchemy
DB_URI = "postgresql:///dancers2"
db = SQLAlchemy()

""" Model Definitions """

class User(db.Model):
    """User"""

    __tablename__ = "users"


    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(64), nullable = False, unique=True)
    email = db.Column(db.String(64), nullable = False, unique=True)
    password = db.Column(db.String(64), nullable = False)


    def __repr__(self):
        """Provide helpful information when printed."""

        return f"""<User user_id={self.user_id} user_name={self.user_name} 
                email={self.email} password= {self.password}>"""

class Class(db.Model):
    """Class"""

    __tablename__ = "classes"


    class_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    class_name = db.Column(db.String(130), nullable = False, unique=True)
    start_time = db.Column(db.TIMESTAMP(timezone=True))
    end_time = db.Column(db.TIMESTAMP(timezone=True))
    url = db.Column(db.String(300))

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
    class_saved = db.Column(db.Boolean)
    class_attended = db.Column(db.Boolean)

    user = db.relationship("User", backref="user_classes") 
    dance_class = db.relationship("Class", backref="user_classes")

    def __repr__(self):
        """Provide helpful information when printed."""

        return f"""<UserClass user_class_id={self.user_class_id} 
            user_id={self.user_id} class_id={self.class_id} 
            class_saved={self.class_saved} class_attended={self.class_attended}>"""    


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dancers2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
 

    from server import app
    connect_to_db(app)
    print("Connected to DB.")  