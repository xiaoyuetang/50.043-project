from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, ReviewForm
from flask_login import current_user, login_user
from app import db
from app.models import User, Trial
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required


@app.route('/')
@app.route('/index')
@login_required
def index():
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}		
	]
	author = "author1"
	book_title = "book1"
	#return render_template('index.html', title='home', posts=posts)
	return render_template('bookreview.html', author = author, book_title = book_title)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

#@app.route('/bookreviews')
#def bookreviews():
#	return render_template('bookreview.html')
	
@app.route('/addbook')
def addbook():
	return render_template('addbook.html')

@app.route('/addreview', methods=['GET', 'POST'])
@login_required
def addreview():
	form = ReviewForm()
	if form.validate_on_submit():
		reviewID = Trial.query.filter_by(reviewID=form.reviewID.data).first()
		if reviewID is not None:
			flash('reviewerID already existed')
			return redirect(url_for('addreview'))

		reviewID = form.reviewID.data
		overall = form.overall.data
		reviewText = form.reviewText.data
		
		# add review to database
		review = Trial(reviewID=reviewID, overall=overall, reviewText=reviewText)
		db.session.add(review)
		db.session.commit()
		
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('add_review.html', title='Add a Review', form=form)

@app.route('/book_review', methods=['GET', 'POST'])
@login_required
def book_review():
	form = ReviewForm()
	if form.validate_on_submit():
		reviewID = Trial.query.filter_by(reviewID=form.reviewID.data).first()
		if reviewID is not None:
			flash('reviewerID already existed')
			return redirect(url_for('book_review'))

		reviewID = form.reviewID.data
		overall = form.overall.data
		reviewText = form.reviewText.data
		
		# add review to database
		review = Trial(reviewID=reviewID, overall=overall, reviewText=reviewText)
		db.session.add(review)
		db.session.commit()
		
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('book_review.html', title='Add a Review', form=form)
