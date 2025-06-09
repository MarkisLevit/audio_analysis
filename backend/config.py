from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///audio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False 

db=SQLAlchemy(app)