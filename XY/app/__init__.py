from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.config['MONGOALCHEMY_DATABASE'] = 'log'

db = SQLAlchemy(app)
log = MongoAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
