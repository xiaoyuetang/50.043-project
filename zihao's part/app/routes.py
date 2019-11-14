from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, ReviewForm
from flask_login import current_user, login_user
from app import db
from app.models import User, Trial, Review, ReviewerReviews, ReviewerInformation
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required



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

####################### below are revisited version ########################

# main page
# html file: index.html
# 我把左上角的logo暂定为点了以后进到某个书的 review page
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	
# 看到书的 Description / 可以 write a review
@app.route("/review")
def review():
	'''
	Using dummy data for now. Fetch from DB next time.
	'''

	''' Dummy Main Book '''
	title = "The Arsonist"
	cover = "https://www.booktopia.com.au/blog/wp-content/uploads/2018/12/the-arsonist.jpg"
	desc = "Sed iaculis posuere diam ut cursus. assa magna, vulputate nec bibendum nec, posuere nec lacus. Sed iaculis posuere diam ut cursus. assa magna, vulputate nec bibendum nec, posuere nec lacus. Sed iaculis posuere diam ut cursus. assa magna, vulputate nec bibendum nec, posuere nec lacus. Sed iaculis posuere diam ut cursus. assa magna, vulputate nec bibendum nec, posuere nec lacus."
	author = "Chloe Hooper"
	tags = ["Fantasy", "Romance", "Cookbooks"]

	main_book = {"title": title, "cover": cover,
				 "desc": desc, "author": author, "tags": tags}

	''' Dummy reviews '''
	name1 = "Jane P."
	img1 = "https://media.istockphoto.com/photos/portrait-of-a-smiling-young-woman-picture-id905456806?k=6&m=905456806&s=612x612&w=0&h=PvYHS82wm1FlEh7_8Owj_OamqJfJ8g3igDrfbA4Xo7I="
	text1 = "Good Book!"
	summary1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget sapien sapien. Curabitur in metus urna. In hac habitasse platea dictumst. Phasellus eu sem sapien, sed vestibulum velit. Nam purus nibh, lacinia non faucibus"
	overall1 = 4
	review1 = {"name": name1, "img": img1, "text": text1,
			   "summary": summary1, "overall": overall1}

	reviews = [review1, review1, review1, review1, review1, review1]

	''' Dummy Related books '''
	cover1 = "https://marketplace.canva.com/MADSMNPt8uA/3/0/thumbnail_large/canva-green-beach-photo-book-cover-MADSMNPt8uA.jpg"
	title1 = "The Sun in His Eyes"
	author1 = "Eleanor Fitzgerald"
	tags1 = ["Sports", "Cookbooks", "Psychology", "Biography"]
	related1 = {"cover": cover1, "title": title1,
				"author": author1, "tags": tags1}

	relateds = [related1, related1, related1]
	
	return render_template("review-page.html", main=main_book, reviews=reviews, relateds=relateds)


@app.route("/review", methods=["POST"])
@login_required
def submit_review():
	'''
	Get the header and review from review form and do something upon submit
	'''
	if request.form['button'] == "Log In":
		return render_template("index.html")
	elif request.form['button'] == "Submit Review":
		text = request.form['reviewText']
		summary = request.form['reviewSummary']
		
		print (type(text))
		print (type(summary))
		
		# store the review into database
		new_review = Review(reviewID='20')
		db.session.add(new_review)
		db.session.commit()
		
		return render_template("thank-you.html")
	else:
		return "Hello"


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
