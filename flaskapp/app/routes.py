from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, ReviewForm, RegistrationForm
from app import db, meta, con
from app.models import User, Review, ReviewerReviews, ReviewerInformation
from werkzeug.urls import url_parse
from datetime import datetime, date, time
import matplotlib.pyplot as plt

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

@app.route('/',methods=['GET', 'POST'])
# @app.route('/index')
def index():

	############

	# top10_review = Review.query.filter_by(overall=5).limit(35).all()
	# top10_review_asin = []
	# for i in top10_review:
	# 	reviewerReviews = ReviewerReviews.query.filter_by(reviewID=i.reviewID).first()
	# 	top10_review_asin.append(reviewerReviews.asin)
	# top10_review_asin = list(dict.fromkeys(top10_review_asin))
	cur = con.cursor()
	cur.execute("select distinct asin from KindleReview where overall=5 limit 27")
	data = cur.fetchall()
	result =[]
	for i in data:
		result.append(i[0])

	############
	BookInfoList = []
	BookList=[]
	for i in range(len(result)):
		booki = meta.db.metaKindleStoreClean.find_one({"asin":result[i],'imUrl':{'$exists': True},'description':{'$exists': True},'categories':{'$exists':True}})

		if booki != None and len(BookInfoList) <=10:
			BookInfoList.append(booki)
	##########query new arrivals#########
	newArrivalsTemp = meta.db.metaKindleStoreClean.find({"asin":{'$exists': True},"title":{'$exists': True},"description":{'$exists': True},"categories":{'$exists': True},"imUrl":{'$exists': True},"author":{'$exists': True}})
	newArrivals = []
	for i in newArrivalsTemp:
		newArrivals.append(i)

	################search here#########
	search_input = None
	if request.method == 'POST' and request.form['search-btn'] == 'Search':
		search_input = request.form['search-input']
		return redirect(url_for('search', search_input=search_input))
	TagList=['Science Fiction', 'satire', 'drama', 'Action and Adventure', 'Romance', 'mystery', 'horror', 'self help', 'guide',
	'travel', "children's", 'religious', 'science', 'history', 'math', 'anthologies', 'poetry', 'encyclopedia', 'dictionaries', 'comics',
	'art', 'cookbooks', 'diaries', 'prayer books', 'series', 'trilogies', 'biographies', 'autobiographies', 'fantasy']

	return render_template('index.html',BookInfoList = BookInfoList,newArrivals = newArrivals,TagList=TagList)


@app.route('/search-result',methods=['GET', 'POST'])
@login_required
def search():
    # search_input = request.args['search_input']
    search_input = request.args.get('search_input')
    results = search_book(search_input)
    add_log("searchbook", "", search_input,  "search book successfully", current_user.username)
    return render_template('search-result.html', search_input=search_input, search_results = results)

def search_book(keyword):
	query = {'$or':[{'title':{"$regex":keyword,"$options":"i"}},{'author':{"$regex":keyword,"$options":"i"}},

			{'brand':{"$regex":keyword, "$options":"i"}},{'asin':{"$regex":keyword, "$options":"i"}},

			{'categories': {'$elemMatch': {'$elemMatch': {"$regex":keyword, "$options":"i"}}}}]}
	cursor = meta.db.metaKindleStoreClean.find(query)
	results = [book for book in cursor]
	print(results)
	return results

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

# @app.route("/review", methods=["POST"])
# @login_required
# def submit_review():

# 	if request.form['button'] == "Log In":
# 		return render_template("index.html")
# 	elif request.form['button'] == "Submit Review":
# 		text = request.form['reviewText']
# 		summary = request.form['reviewSummary']

# 		# store the review into database
# 		new_review = Review(reviewID='20', reviewText=text, summary=summary)
# 		db.session.add(new_review)
# 		db.session.commit()

# 		return render_template("thank-you.html")
# 	else:
# 		return "Hello"

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
@app.route("/review", methods = ['GET', 'POST'])
def review():
	asin = request.args.get('asin')
	book = meta.db.metaKindleStoreClean.find_one({"asin":asin})
	if 'title'in book:
		title = book['title']
	else:
		title = book['asin']
	cover = book['imUrl']
	desc = book['description']
	tagslist = book['categories']
	if 'author'in book:
		author = book['author']
	else:
		author = '2333'
	tags=[]
	if type(tagslist)==list:
		for i in tagslist:
			for j in i:
				if j in tags:
					i.remove(j)
			tags.extend(i)
	else:
		tags.append(tagslist)

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

	##### Review submission #####
	form = request.form
	if request.method == "POST":
		'''
		Check for login. Not sure if this is correct.
		'''
		if not current_user.is_authenticated:
			return redirect(url_for('login'))
		if 'reviewbutton' in form:
			id = 000000  # NEED HELP HERE
			reviewID = 0  # NEED HELP HERE
			# asin is pulled already
			print("ASIN IS ", asin)
			overall = form['overall'].count("\u2605")  # count number of stars
			reviewText = form['reviewText']
			reviewTime = get_review_time()
			reviewerID = "A29cDXC"  # NEED TO GET FROM DB
			reviewerName = "ASDADS"  # NEED TO GET FROM DB
			summary = form['summary']
			unixReviewTime = int(datetime.utcnow().timestamp())
			'''
			Push to DB here !!!
			'''
			print("DONE PUSHING")
			add_log("addreview",request.method, asin, "add review successfully", current_user.username)
	#### ####

	#### Load Reviews from DB ####
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
	count=0
	for i in relatedlist:
		book = meta.db.metaKindleStoreClean.find_one({"asin":i})
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
	BookAsin = request.form['BookAsin']
	BookImUrl = request.form['BookImUrl']
	MoreAbtBook = request.form["MoreAbtBook"]
	# Save book information to the mongoDB
	# mydict = {'ClientName':ClientName,
	# 'ClientEmail':ClientEmail,
	# 'categories':BookCat,
	# 'asin':BookAsin,
	# 'title':BookName,
	# 'author':BookAuthor,
	# 'imUrl':BookImUrl,
	# 'description':MoreAbtBook}
	meta.db.metaKindleStoreClean.find_one_and_update({"asin": BookAsin},
                               {"$set": {"title": BookName,"author": BookAuthor,"imUrl": BookImUrl,"description": MoreAbtBook,"categories": BookCat}},upsert=True)
	add_log("addbook",request.method, request.url, "add book successfully", current_user.username)
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

def get_review_time():
	today = date.today()
	year = str(today.year)
	month = str(today.month)
	day = str(today.day)

	return month + " " + day + ", " + year


def add_log(request_summary, request_type, request_content, response, user_name, time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), year = str(date.today().year), month = str(date.today().month), day= str(date.today().day)):
	logInfo = {'TimeStamp':time_stamp,
	'RequestSummary': request_summary,
	'RequestType':request_type,
	'RequestContent':request_content,
	'Response':response,
	'UserName':user_name,
	'Year':year,
	'Month':month,
	'Day':day}
	meta.db.systemLog.insert(logInfo)
	# log.db.systemLog.insert(logInfo)

@app.route("/TodayHistory")
@login_required
def log_page():
	logIT = meta.db.systemLog.find({"Day": {'$eq':str(date.today().day)},"Year": {'$eq':str(date.today().year)}, "Month":{'$eq':str(date.today().month)}})

	logInfoToday =[]
	for i in logIT:
		logInfoToday.append(i)
	return render_template("logtoday.html", logInfoToday = logInfoToday)


def search_plot():
	logMonth = meta.db.systemLog.find({"Year": {'$eq':str(date.today().year)}, "Month":{'$eq':str(date.today().month)}})
	monthStats = {}
	for m in logMonth:
		if "searchbook" in m.values():
			monthStats[m['RequestContent']] = 1+ monthStats.get(m['RequestContent'],0)

	sort_value = sorted(monthStats.values())
	top_x = []
	top_y = []

	for key in monthStats:

		if monthStats[key] in sort_value[0:10]:
			top_x.append(key)
			top_y.append(monthStats[key])
	plt.bar(top_x,top_y)
	plt.title("Top 10 most popular books for review")

	plt.savefig("topReview.png")
	#plt.show()
def review_plot():
	logMonth = meta.db.systemLog.find({"Year": {'$eq':str(date.today().year)}, "Month":{'$eq':str(date.today().month)}})
	monthStats = {}
	for m in logMonth:
		if "addreview" in m.values():

			monthStats[m['RequestContent']] = 1+ monthStats.get(m['RequestContent'],0)
	sort_value = sorted(monthStats.values())
	top_x = []
	top_y = []
	for key in monthStats:
		if monthStats[key] in sort_value[0:10]:
			top_x.append(key)
			top_y.append(monthStats[key])
	plt.bar(top_x,top_y)
	plt.title("Top 10 most searched words")

	plt.savefig("topSearch.png")
	#plt.show()

@app.route("/statsPlot")
@login_required
def month_Stats():
	search_plot()
	review_plot()
	return render_template("StatsPlot.html")
