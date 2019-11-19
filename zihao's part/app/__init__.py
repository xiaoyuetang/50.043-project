from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo

import logging
import logging.handlers

ssh_address='ec2-52-42-232-25.us-west-2.compute.amazonaws.com'
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.config['MONGOALCHEMY_DATABASE'] = 'log'
app.config["MONGO_URI"] = "mongodb://books:123456789@"+ssh_address+":27017/books"

db = SQLAlchemy(app)
log = MongoAlchemy(app)
migrate = Migrate(app, db)
meta = PyMongo(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
from app.models import SystemLog

class MongoAlchemyHandler(logging.Handler):
	def emit(self, record):
		trace = None
		exc = record.__dict__['exc_info']
		if exc:
			trace = traceback.format_exc() ##CHANGE HERE, removed exc parameter
		message = record.__dict__['msg']
		request_index = 0
		response_index = -2
		if 'GET' in message:
			request_index = message.find('GET')
		if 'POST' in message:
			request_index = message.find('POST')

		req = message[request_index:-1]
		if '"' in req and request_index != 0:

			response_index = req.find('"')

		log = SystemLog(
	        request = req[0:response_index],
	        response = req[response_index+1:-1])
		log.save()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = MongoAlchemyHandler()
ch.setLevel(logging.INFO)

loggers = [logger, logging.getLogger('werkzeug'), logging.getLogger('flask.app')]

for l in loggers:
	l.addHandler(ch)
