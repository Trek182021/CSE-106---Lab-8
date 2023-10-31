from flask import Flask
from flask_cors import CORS
from classes import db, admin
from api import api

app = Flask(__name__)
app.register_blueprint(api)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config["SECRET_KEY"] = 'mysecret'

db.init_app(app)
admin.init_app(app)
    
if __name__ == '__main__':
    app.run()
    
