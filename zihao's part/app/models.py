from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_bash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	
	def __repr__(self):
		return '<User {}>'.format(self.username)
		
	def set_password(self, password):
		self.password_bash = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password_bash, password)
		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post {}>'.format(self.body)

class ReviewerInfomation(db.Model):
	reviewerID = db.Column(db.String(64), primary_key=True)
	reviewerName = db.Column(db.String(64), index=True)
	
	def __repr__(self):
		return '<Reviewer: {}>'.format(self.reviewerName)

class Review(db.Model):
	reviewID = db.Column(db.Integer, primary_key=True)
	helpful_1 = db.Column(db.String(64), index=True)
	helpful_2 = db.Column(db.String(64), index=True)
	overall = db.Column(db.Integer, index=True)
	reviewText = db.Column(db.String(128), index=True)
	summary = db.Column(db.String(64), index=True)
	unixReviewTime = db.Column(db.Integer, index=True)

	def __repr__(self):
		return '<Review ID: {}>'.format(self.reviewID)

class ReviewerReviews(db.Model):
	reviewID = db.Column(db.Integer, primary_key=True)
	asin = db.Column(db.String(64), index=True)
	reviewerID = db.Column(db.String(64), db.ForeignKey('reviewerinformation.reviewerID'))
	
	def __repr__(self):
		return '<Review ID: {}, Review product: {}, Reviewer ID: {}>'.format(self.reviewID, self.asin, self.reviewerID)

class Trial(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	reviewID = db.Column(db.Integer, primary_key=True)
	asin = db.Column(db.String(64), index=True)
	overall = db.Column(db.Integer, index=True)
	reviewText = db.Column(db.String(128), index=True)
	reviewTime = db.Column(db.String(128), index=True)
	reviewerID = db.Column(db.String(64), index=True)
	reviewerName = db.Column(db.String(64), index=True)
	summary = db.Column(db.String(64), index=True)
	unixReviewTime = db.Column(db.Integer, index=True)
	
	def __repr__(self):
		return '<Review ID: {}>'.format(self.reviewID)
	

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
