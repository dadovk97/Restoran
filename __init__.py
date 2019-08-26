from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab1f5c1c91a80a6f84c848f410971f72'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restoran.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'Prijava'
login_manager.login_message_category = 'info'

from restoran import routes