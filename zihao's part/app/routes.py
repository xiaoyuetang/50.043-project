from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, ReviewForm, RegistrationForm
from app import db, log, meta
from app.models import User, Review, ReviewerReviews, ReviewerInformation
from werkzeug.urls import url_parse
from datetime import datetime

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

####################### below are revisited version ########################

@app.route('/')
@app.route('/index')
def index():
	
	############
	
	top10_review = Review.query.filter_by(overall=5).limit(25).all()
	top10_review_asin = []
	for i in top10_review:
		reviewerReviews = ReviewerReviews.query.filter_by(reviewID=i.reviewID).first()
		top10_review_asin.append(reviewerReviews.asin)
	top10_review_asin = list(dict.fromkeys(top10_review_asin))
	
	############
	
	res = meta.db.metaKindleStore.find({'imUrl':{'$exists': True},'description':{'$exists': True},'categories':{'$exists':True}},{'asin':1,'categories':1,'imUrl':1,'title':1,'description':1,'_id':0}).limit(6)
	BookInfoList = []
	for i in res:
		for j in i["categories"]:
			for k in j:
				if 'Books' in k or 'Kindle eBooks' in k:
					if i not in BookInfoList:
						BookInfoList.append(i)
	return render_template('index.html',BookInfoList = BookInfoList)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	if request.method == 'POST':
		if request.form['loginbutton'] == 'Log In':

			userid = request.form['userid']
			password = request.form['password']
			user = User.query.filter_by(username=userid).first()
			if user is None or not user.check_password(password):
				flash('Invalid username or password')
				return redirect(url_for('login'))
			remember = request.form["loginsavepw"]
			login_user(user, remember=remember)
			next_page = request.args.get('next')
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('index')
			return redirect(next_page)
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	if request.method == 'POST':
		if request.form['signupbutton'] == 'Sign up':
			userid = request.form['new_username']
			email = request.form['new_email']
			password = request.form['new_password']

			user = User(username=userid, email=email)
			user.set_password(password)
			db.session.add(user)
			db.session.commit()
			flash('Congratulations, you are now a registered user!')
			return redirect(url_for('index'))
	return render_template('signup.html', title='Register')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/review", methods=["POST"])
@login_required
def submit_review():

	if request.form['button'] == "Log In":
		return render_template("index.html")
	elif request.form['button'] == "Submit Review":
		text = request.form['reviewText']
		summary = request.form['reviewSummary']

		# store the review into database
		new_review = Review(reviewID='20', reviewText=text, summary=summary)
		db.session.add(new_review)
		db.session.commit()

		return render_template("thank-you.html")
	else:
		return "Hello"

# save the latest log records to database
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

# edit user profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

# Description / write a review
@app.route("/review", methods = ['GET'])
def review():
	asin = request.args.get('asin')
	book = meta.db.metaKindleStore.find_one({"asin":asin})
	title = book['asin']
	cover = book['imUrl']
	desc = book['description']
	tagslist = book['categories']
	author = '2333'
	tags=[]
	for i in tagslist:
		for j in i:
			if j in tags:
				i.remove(j)
		tags.extend(i)

	main_book = {"title": title, "cover": cover,
				 "desc": desc, "author": author, "tags": tags}
	relateds=[]
	relatedlist=[]

	if 'also_viewed' in book['related']:
		relatedlist = book['related']['also_viewed']
		# relateds = bookinfo(relatedlist)
	elif book['related']['also_bought'] is not None:
		relatedlist = book['related']['also_bought']
		# relateds = bookinfo(relatedlist)
	elif 'buy_after_viewing' in book['related']:
		relatedlist = book['related']['buy_after_viewing']

	if len(relatedlist)!=0:
		relateds = bookinfo(relatedlist)

	#################
	review_reviews = ReviewerReviews.query.filter_by(asin=asin).limit(10).all()
	review_ids = []
	for i in review_reviews:
		review_ids.append(i.reviewID)
	records = Review.query.filter(Review.reviewID.in_(review_ids)).all()

	reviews = []
	for i in records:
		name = 'Small Bling Bling'
		img = 'https://media.istockphoto.com/photos/portrait-of-a-smiling-young-woman-picture-id905456806?k=6&m=905456806&s=612x612&w=0&h=PvYHS82wm1FlEh7_8Owj_OamqJfJ8g3igDrfbA4Xo7I='
		summary = i.summary
		text = i.reviewText
		overall = i.overall
		
		review = {"name": name, "img": img, "text": text, "summary": summary, "overall": overall}
		reviews.append(review)
	##################

	return render_template("review-page.html", main=main_book, reviews=reviews, relateds=relateds)

def bookinfo(relatedlist):
	relateds=[]
	print(relatedlist)
	count=0
	for i in relatedlist:
		print(i)
		book = meta.db.metaKindleStore.find_one({"asin":i})
		if book is not None:

			if 'imUrl' in book:
				title=book['asin']
				cover=book['imUrl']
				author='2333'
				tagslist = book['categories']
				tags=[]
				for j in tagslist:
					for k in j:
						if k in tags:
							j.remove(k)
					tags.extend(j)
				related = {"cover": cover, "title": title,
						"author": author, "tags": tags}
				relateds.append(related)
				count+=1
		if count==5:
			break
	return relateds

# add-a-book page
@app.route("/add-a-book")
@login_required
def add_a_book():
	return render_template("add-a-book.html")

# add a new book upon submit
@app.route("/add-a-book", methods=['POST'])
@login_required
def submit_book_info():

	# Get the book info from add-a-book form
	ClientName = request.form['ClientName']
	ClientEmail = request.form['ClientEmail']
	BookCat = request.form["BookCat"]
	BookName = request.form["BookName"]
	BookAuthor = request.form["BookAuthor"]
	MoreAbtBook = request.form["MoreAbtBook"]
	# Save book information to the mongoDB
	mydict = {'ClientName':ClientName,
	'ClientEmail':ClientEmail,
	'BookCat':BookCat,
	'BookName':BookName,
	'BookAuthor':BookAuthor,
	'MoreAbtBook':MoreAbtBook}
	meta.db.newbooks.insert(mydict)

	return render_template("thank-you.html")

@app.route("/history")
@login_required
def history():
	'''
	Using dummy data for now. Fetch from DB next time.
	'''
	b1 = "Harry Potter"
	c1 = "https://img1-placeit-net.s3-accelerate.amazonaws.com/uploads/stage/stage_image/39885/large_thumb_book-cover-horror-novel-527.jpg"
	a1 = "A. Dinh"
	tags1 = ["Art", "Cookbooks"]
	book1 = {"title": b1, "cover": c1, "author": a1, "tags": tags1}

	b2 = "Rich Dad Poor Dad"
	c2 = "https://img2-placeit-net.s3-accelerate.amazonaws.com/uploads/stage/stage_image/37837/large_thumb_stage.jpg"
	a2 = "B. Dinh"
	tags2 = ["Self Help", "Thriller", "Graphic Novels"]
	book2 = {"title": b2, "cover": c2, "author": a2, "tags": tags2}

	b3 = "Lord of The Rings"
	c3 = "https://i.pinimg.com/236x/82/79/74/827974d98ed5dabfbeecbdae890caebf.jpg"
	a3 = "C. Dinh"
	tags3 = ["Business", "Fiction", "Nonfiction"]
	book3 = {"title": b3, "cover": c3, "author": a3, "tags": tags3}

	books = [book1, book2, book3]

	return render_template("history.html", books=books)

@app.route("/profile")
# @app.route("/profile/<username>")
@login_required
def profile():
# def profile(username):

	#user = User.query.filter_by(username=username).first_or_404()
	# 相关的信息需要什么
	# posts =
	# reviews =

	return render_template("profile.html")
