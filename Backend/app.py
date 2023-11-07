from flask import Flask, render_template, redirect, url_for, request, flash
from flask_cors import CORS
from classes import db, admin, User
from api import api
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flask_login import current_user, login_user, logout_user, LoginManager
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/signin', methods= ['POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))


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
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the 
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password")
            print("INVALID!!!!!!!!!!!!!!")
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run()
    
