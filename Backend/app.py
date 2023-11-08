from flask import Flask, render_template, redirect, url_for, request, flash
from flask_cors import CORS
from classes import db, admin, User
from api import api
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from api import *
import json
# import get_routes

app = Flask(__name__)
app.register_blueprint(api)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config["SECRET_KEY"] = 'mysecret'

db.init_app(app)
admin.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'


@login_manager.unauthorized_handler
def unauthorized():
    flash("You are not authenticated. Please login")
    return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        user = User(name=request.form.get("username"),
                    username=request.form.get("username"),
                    password=request.form.get("password"),
                    role_id = 1)
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by 
    # filtering for the username
    print("LOG", request.method)
    if request.method == "POST":
        print("POSTTT")
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the 
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            print("SUCCESS!!!")
            if (user.role.name == "Student"):
                return redirect(url_for('studentsPage'))
            elif (user.role.name == "Admin"):
                return redirect("/admin")
        else:
            flash("Invalid username or password")
            print("INVALID!!!!!!!!!!!!!!")

        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    # return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/students")
@login_required
def studentsPage():
    data = getCourses(current_user.id)
    data2 = getStudentCourses(current_user.id)
    studentCourses = data2.json
    allCourses = data.json
    return render_template("students.html", studentCourses=studentCourses, allCourses=allCourses)

if __name__ == '__main__':
    app.run()
    
