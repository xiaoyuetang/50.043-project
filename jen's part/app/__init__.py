from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL

import logging
import logging.handlers
from urllib import parse
pwd = parse.quote("123456789@")
ssh_address1='ec2-52-42-232-25.us-west-2.compute.amazonaws.com'
ssh_address2="ec2-54-227-63-130.compute-1.amazonaws.com"
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.config['TESTING'] = True
logging.basicConfig(level=logging.DEBUG)
app.config['MYSQL_HOST'] = 'bigdhatta.ceerfqdva59u.ap-southeast-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'J3reakD0wn'
app.config['MYSQL_DB'] = 'reviews'
mysql = MySQL(app)



meta = PyMongo(app,uri="mongodb://books:123456789@"+ssh_address1+":27017/books")
log = PyMongo(app,uri="mongodb://logadmin:"+pwd+"@"+ssh_address2+":27017/log")

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'




from app import routes, models, errors


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

		mydict= {
			"timestamp" : datetime.utcnow(),
	        "request" : req[0:response_index],
	        "response" : req[response_index+1:-1]}

		log.db.systemLog.insert(mydict)






logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = MongoAlchemyHandler()
ch.setLevel(logging.INFO)

loggers = [logger, logging.getLogger('werkzeug'), logging.getLogger('flask.app')]

for l in loggers:
	l.addHandler(ch)
