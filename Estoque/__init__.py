from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'logar'
login_manager.login_message_category = 'alert-info'

from Estoque import routes