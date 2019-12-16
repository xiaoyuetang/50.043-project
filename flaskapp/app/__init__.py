from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo
import mysql.connector as sqldb
import logging
import logging.handlers
from urllib import parse
import os
pwd = parse.quote("123456789@")
################

# metaIp=os.environ['mongodb_ip']
# mysqlIp=os.environ['mysql_ip']
# logIp=os.environ['logmongod_ip']
# con= sqldb.connect(host=mysqlIp, user="root", passwd="", db="flaskproject")
# meta = PyMongo(app,uri="mongodb://books:123456789@"+metaIp+":27017/books")
# log = PyMongo(app,uri="mongodb://logadmin:"+pwd+"@"+logIp+":27017/log")
#################

ssh_address1='ec2-52-42-232-25.us-west-2.compute.amazonaws.com'
ssh_address2="ec2-52-207-113-15.compute-1.amazonaws.com"
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

# addr = 'bigdhatta.ceerfqdva59u.ap-southeast-1.rds.amazonaws.com'
# mysql = MySQL(app)
ec2host='ec2-34-220-172-38.us-west-2.compute.amazonaws.com'
# ec2host='54.189.148.212'
con= sqldb.connect(host=ec2host, user="root", passwd="", db="flaskproject")
meta = PyMongo(app,uri="mongodb://books:123456789@"+ssh_address1+":27017/books")
log = PyMongo(app,uri="mongodb://logadmin:"+pwd+"@"+ssh_address2+":27017/log")

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors


# class MongoAlchemyHandler(logging.Handler):
# 	def emit(self, record):
# 		trace = None
# 		exc = record.__dict__['exc_info']
# 		if exc:
# 			trace = traceback.format_exc() ##CHANGE HERE, removed exc parameter
# 		message = record.__dict__['msg']
# 		request_index = 0
# 		response_index = -2
# 		if 'GET' in message:
# 			request_index = message.find('GET')
# 		if 'POST' in message:
# 			request_index = message.find('POST')

# 		req = message[request_index:-1]
# 		if '"' in req and request_index != 0:

# 			response_index = req.find('"')

# 		mydict= {
# 			"timestamp" : datetime.utcnow(),
# 	        "request" : req[0:response_index],
# 	        "response" : req[response_index+1:-1]}

# 		log.db.systemLog.insert(mydict)






# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# ch = MongoAlchemyHandler()
# ch.setLevel(logging.INFO)

# loggers = [logger, logging.getLogger('werkzeug'), logging.getLogger('flask.app')]

# for l in loggers:
# 	l.addHandler(ch)

# if __name__ == "__main__":
# 	app.run(host="0.0.0.0", port=80)
