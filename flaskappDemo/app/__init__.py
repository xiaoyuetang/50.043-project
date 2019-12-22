from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL
import mysql.connector as sqldb
import logging
import logging.handlers
import os

####for automation script######
################
# file = open('ip.txt','r')
# for line in file:
#     ips=line.split(' ')
#     mysqlIp=ips[0]
#     metaIp=ips[1]
################


#################

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

######################################################################
# con= sqldb.connect(host=mysqlIp, user="root", passwd="", db="flaskproject")
# meta = PyMongo(app,uri="mongodb://books:123456789@"+metaIp+":27017/books")
#########################################################################
ec2host='35.160.25.169'
ssh_address1='34.217.109.132'

app.config['MYSQL_HOST']=ec2host
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskproject'
mysql=MySQL(app)
#con = mysql.connection.cursor()
#con= sqldb.connect(host=ec2host, user="root", passwd="", db="flaskproject")
meta = PyMongo(app,uri="mongodb://books:123456789@"+ssh_address1+":27017/books")


db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors


