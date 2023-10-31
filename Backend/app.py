from flask import Flask
from flask_cors import CORS
from classes import db, admin
from api import api
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flask_login import current_user, login_user
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
    return User.get_id(user_id)

@app.route('/signin', methods= ['POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    
