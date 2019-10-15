from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class ReviewForm(FlaskForm):
	reviewID = StringField('reviewID', validators=[DataRequired()])
	overall = IntegerField('overall rating', validators=[DataRequired()])
	reviewText = StringField('review', validators=[DataRequired()])
	submit = SubmitField('Submit Review')