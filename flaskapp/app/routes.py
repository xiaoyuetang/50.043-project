from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, ReviewForm, RegistrationForm
from app import db, meta, con
from app.models import User, Review, ReviewerReviews, ReviewerInformation
from werkzeug.urls import url_parse
from datetime import datetime, date, time, timedelta
from mysql.connector import MySQLConnection, Error
import random
import string


####################### below are revisited version ########################

@app.route('/', methods=['GET', 'POST'])
# @app.route('/index')
def index():

    ############
    cur = con.cursor()
    cur.execute(
        "select distinct asin from KindleReview where overall=5 limit 27")
    data = cur.fetchall()
    result = []
    for i in data:
        result.append(i[0])

    ############
    BookInfoList = []
    BookList = []
    for i in range(len(result)):
        booki = meta.db.metaKindleStoreClean.find_one({"asin": result[i], 'imUrl': {
                                                      '$exists': True}, 'description': {'$exists': True}, 'categories': {'$exists': True}})

        if booki != None and len(BookInfoList) <= 10:
            BookInfoList.append(booki)
    ############query top 20#########
    topbook = meta.db.metaKindleStoreClean.find({'imUrl': {'$exists': True}, 'description': {
                                                '$exists': True}, 'categories': {'$exists': True}}).limit(20)
    TopBooks = []
    for i in topbook:
        TopBooks.append(i)

    ##########query new arrivals#########
    newArrivalsTemp = meta.db.metaKindleStoreClean.find({"asin": {'$exists': True}, "title": {'$exists': True}, "description": {
                                                        '$exists': True}, "categories": {'$exists': True}, "imUrl": {'$exists': True}, "author": {'$exists': True}})
    newArrivals = []
    for i in newArrivalsTemp:
        newArrivals.append(i)
    ##########query reviews##########
    cur = con.cursor()
    cur.execute("select reviewerName,reviewText from KindleReview limit 10;")
    myresult = cur.fetchall()
    con.commit()

    ################search here#########
    search_input = None
    if request.method == 'POST' and request.form['search-btn'] == 'Search':
        search_input = request.form['search-input']
        return redirect(url_for('search', search_input=search_input))
    TagList = ['Science Fiction', 'satire', 'drama', 'Action and Adventure', 'Romance', 'mystery', 'horror', 'self help', 'guide',
               'travel', "children's", 'religious', 'science', 'history', 'math', 'anthologies', 'poetry', 'encyclopedia', 'dictionaries', 'comics',
               'art', 'cookbooks', 'diaries', 'prayer books', 'series', 'trilogies', 'biographies', 'autobiographies', 'fantasy']

    return render_template('index.html', BookInfoList=BookInfoList, newArrivals=newArrivals, TagList=TagList, TopBooks=TopBooks, myresult=myresult)


@app.route('/search-result', methods=['GET', 'POST'])
@login_required
def search():
    # search_input = request.args['search_input']
    search_input = request.args.get('search_input')
    results = search_book(search_input)
    if search_input[0:2] == "B0":
        add_log("searchbook", "", search_input,
                "search book successfully", current_user.username)
    # if search_input[0:2] == "B0":
    # add_log("searchbook", "", search_input,  "search book successfully", current_user.username)
    else:
        add_log("searchkeyword", "", search_input,
                "search keyword successfully", current_user.username)
    return render_template('search-result.html', search_input=search_input, search_results=results)


def search_book(keyword):
    query = {'$or': [{'title': {"$regex": keyword, "$options": "i"}}, {'author': {"$regex": keyword, "$options": "i"}},

                     {'brand': {"$regex": keyword, "$options": "i"}}, {
                         'asin': {"$regex": keyword, "$options": "i"}},

                     {'categories': {'$elemMatch': {'$elemMatch': {"$regex": keyword, "$options": "i"}}}}]}
    cursor = meta.db.metaKindleStoreClean.find(query)
    results = [book for book in cursor]
    print(results)
    return results


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You have already logged in!")
        return render_template('already_login.html')

    if request.method == 'POST':
        if request.form['loginbutton'] == 'Log In':

            userid = request.form['userid']
            password = request.form['password']
            user = User.query.filter_by(username=userid).first()
            if user is None or not user.check_password(password):
                flash('Invalid username or password')
                return redirect(url_for('login'))

            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You have already logged in!")
        return render_template('already_login.html')

    if request.method == 'POST':
        if request.form['signupbutton'] == 'Sign up':
            username = request.form['new_username']
            email = request.form['new_email']
            password = request.form['new_password']

            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('index'))
    return render_template('signup.html', title='Register')


# @app.route('/', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         flash("You have already logged in!")
#         return render_template('already_login.html')

#     if request.method == 'POST':
#         if request.form['signupbutton'] == 'Sign up':
#             userid = request.form['new_username']
#             email = request.form['new_email']
#             password = request.form['new_password']

#             user = User(username=userid, email=email)
#             user.set_password(password)
#             db.session.update(user).where(user.username=str(current_user.username)).values(name=new_username)
#             db.session.commit()
#             flash('Congratulations, you are now a registered user!')
#             return redirect(url_for('index'))
#     return render_template('signup.html', title='Register')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
@app.route("/review", methods=['GET', 'POST'])
def review():
    asin = request.args.get('asin')
    book = meta.db.metaKindleStoreClean.find_one({"asin": asin})
    if 'title'in book:
        title = book['title']
    else:
        title = book['asin']
    if 'description' in book:
        desc = book['description']
    else:
        desc = 'None'
    if 'imUrl' in book:
        cover = book['imUrl']
    else:
        cover = '/static/imag/unknown.jpeg'
    if 'categories' in book:
        tagslist = book['categories']
    else:
        tagslist = []
    if 'author'in book:
        author = book['author']
    else:
        author = '2333'
    tags = []
    if type(tagslist) == list:
        for i in tagslist:
            for j in i:
                if j in tags:
                    i.remove(j)
            tags.extend(i)
    else:
        tags.append(tagslist)

    main_book = {"title": title, "cover": cover,
                 "desc": desc, "author": author, "tags": tags}
    relateds = []
    relatedlist = []
    add_log("viewbook", "", book['asin'],
            "view book successfully", current_user.username)
    if 'related' in book:
        if 'also_viewed' in book['related']:
            relatedlist = book['related']['also_viewed']
            # relateds = bookinfo(relatedlist)
        elif book['related']['also_bought'] is not None:
            relatedlist = book['related']['also_bought']
            # relateds = bookinfo(relatedlist)
        elif 'buy_after_viewing' in book['related']:
            relatedlist = book['related']['buy_after_viewing']

    if len(relatedlist) != 0:
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
            # reviewID = 0  # NEED HELP HERE
            # asin is pulled already

            print("ASIN IS ", asin)
            overall = form['overall'].count("\u2605")  # count number of stars
            reviewText = form['reviewText']
            reviewTime = get_review_time()
            reviewID = "A29cDXC"  # NEED TO GET FROM DB
            reviewerName = "ASDADS"  # NEED TO GET FROM DB
            helpful = '-1'
            summary = form['summary']
            unixReviewTime = int(datetime.utcnow().timestamp())
            '''
			Push to DB here !!!
			'''
            lastid = get_last_id()
            eyed = lastid[0]+1
            result = insert_review(eyed, asin, helpful, overall, reviewText,
                                   reviewTime, reviewID, reviewerName, summary, unixReviewTime)
            print("DONE PUSHING")
            add_log("addreview", request.method, asin,
                    "add review successfully", current_user.username)
            return render_template("thank-you.html")
    #### #### ##############################
    #### Load Reviews from DB ####

    records = catch_reviews(asin)
    reviews = []
    for i in records:
        name = i[0]
        img = 'https://media.istockphoto.com/photos/portrait-of-a-smiling-young-woman-picture-id905456806?k=6&m=905456806&s=612x612&w=0&h=PvYHS82wm1FlEh7_8Owj_OamqJfJ8g3igDrfbA4Xo7I='
        summary = i[1]
        text = i[5]
        overall = i[2]
        print(type(i[3]))
        if type(i[3]) == str:
            helpful = [int(j) for j in i[3].strip('[]').split(',')]
            print(helpful[0])
        else:
            helpful = [0, 0]
        review = {"name": name, "img": img, "text": text,
                  "summary": summary, "overall": overall, "helpful": helpful}
        reviews.append(review)
    ##################

    return render_template("review-page.html", main=main_book, reviews=reviews, relateds=relateds)


def bookinfo(relatedlist):
    relateds = []
    count = 0
    for i in relatedlist:
        book = meta.db.metaKindleStoreClean.find_one({"asin": i})
        if book is not None:

            if 'imUrl' in book:
                title = book['asin']
                cover = book['imUrl']
                author = '2333'
                tagslist = book['categories']
                tags = []
                for j in tagslist:
                    for k in j:
                        if k in tags:
                            j.remove(k)
                    tags.extend(j)
                related = {"cover": cover, "title": title,
                           "author": author, "tags": tags}
                relateds.append(related)
                count += 1
        if count == 5:
            break
    return relateds

# add-a-book page
@app.route("/add-a-book")
@login_required
def add_a_book():
    if str(current_user.username) == "admin":
        return render_template("add-a-book.html")
    else:
        return render_template("admin.html")

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

    meta.db.metaKindleStoreClean.find_one_and_update({"asin": BookAsin},
                                                     {"$set": {"title": BookName, "author": BookAuthor, "imUrl": BookImUrl, "description": MoreAbtBook, "categories": BookCat}}, upsert=True)
    add_log("addbook", request.method, request.url,
            "add book successfully", current_user.username)
    return render_template("thank-you.html")
# add-a-book page
@app.route("/contact")
@login_required
def contact():
    if str(current_user.username) == "admin":
        cusor = meta.db.ContactLog.find()
        print (cusor)
        result = []
        for i in cusor:
            print (i)
            result.append(i)
        return render_template("admin-contact.html", result=result)
    else:
        return render_template("contact.html")
@app.route("/contactDetail",methods=['GET'])
def contactDetail():
    caseId= request.args.get('caseId')
    cusor = meta.db.ContactLog.find_one({'caseId':caseId})
    if request.form["solvebtn"] == 'Solved':
        caseId = str(request.form["caseId"])
        meta.db.ContactLog.find_one_and_update(
            {'caseId': caseId}, {"$set": {"Status": "Solved"}})
    return render_template('contact-detail.html',cusor=cusor)

# add a new book upon submit
@app.route("/contact", methods=['POST', 'GET'])
@login_required
def submit_contact():

    # Get the book info from contact form
    if str(current_user.username) != "admin":
        content = request.form["ContactMe"]
        username = str(current_user.username)
        subject = request.form["ContactTitle"]
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        year = str(date.today().year)
        month = str(date.today().month)
        day = str(date.today().day)
        caseId = ''.join(random.choice(string.digits) for i in range(10))
        contactinfo = {'TimeStamp': time_stamp, 'caseId': caseId,
                       'Username': username,
                       'ContactSubject': subject,
                       'ContactContent': content,
                       'Status': 'Unsolved',
                       'Year': year,
                       'Month': month,
                       'Day': day}
        meta.db.ContactLog.insert(contactinfo)
        print (contactinfo)
        return render_template("thank-you.html")
    else:

        cusor = meta.db.ContactLog.find()
        print (cusor)
        result = []
        for i in cusor:
            print (i)
            result.append(i)

        return render_template("admin-contact.html", result=result)


@app.route("/history")
@login_required
def history():
    logIT = meta.db.systemLog.find({"RequestSummary": {'$eq': "viewbook"}, "UserName": {'$eq': str(current_user.username)},
                                    "Day": {'$eq': str(date.today().day)}, "Year": {'$eq': str(date.today().year)}, "Month": {'$eq': str(date.today().month)}})
    logInfoToday = []
    book = []
    for i in logIT:
        logInfoToday.append(i['RequestContent'])
    logHistory = set(logInfoToday)
    for b in logHistory:
        booki = meta.db.metaKindleStoreClean.find_one({"asin": b})
        book.append(booki)
    return render_template("history.html", book=book)


@app.route("/profile")
# @app.route("/profile/<username>")
@login_required
def profile():
    # def profile(username):

    # user = User.query.filter_by(username=username).first_or_404()
    # posts =
    # reviews =

    return render_template("profile.html")


def get_review_time():
    today = date.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)

    return month + " " + day + ", " + year


def add_log(request_summary, request_type, request_content, response, user_name, time_stamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), year=str(date.today().year), month=str(date.today().month), day=str(date.today().day)):
    logInfo = {'TimeStamp': time_stamp,
               'RequestSummary': request_summary,
               'RequestType': request_type,
               'RequestContent': request_content,
               'Response': response,
               'UserName': user_name,
               'Year': year,
               'Month': month,
               'Day': day}
    meta.db.systemLog.insert(logInfo)
    # log.db.systemLog.insert(logInfo)


@app.route("/TodayHistory")
@login_required
def log_page():
    if str(current_user.username) != "admin":
        return render_template("admin.html")
    else:
        logIT = meta.db.systemLog.find({"Day": {'$eq': str(date.today().day)}, "Year": {
            '$eq': str(date.today().year)}, "Month": {'$eq': str(date.today().month)}})

        logInfoToday = []
        for i in logIT:
            logInfoToday.append(i)
        return render_template("logtoday.html", logInfoToday=logInfoToday)


@app.route("/SevenHistory")
@login_required
def log_seven():
    if str(current_user.username) != "admin":
        return render_template("admin.html")
    else:
        now = datetime.now()
        delta = timedelta(days=7)
        seven_days = now-delta

        logIT = meta.db.systemLog.find({"Day": {'$gte': str(seven_days.day)}, "Year": {
            '$gte': str(seven_days.year)}, "Month": {'$gte': str(seven_days.month)}})
        logInfoSeven = []
        for i in logIT:
            logInfoSeven.append(i)
        return render_template("logseven.html", logInfoSeven=logInfoSeven)


@app.route("/statsPlot")
@login_required
def month_stats():
    # print("???")
    logMonth = meta.db.systemLog.find({"Year": {'$eq': str(
        date.today().year)}, "Month": {'$eq': str(date.today().month)}})
    monthStats_review = {}
    monthStats_search = {}
    monthStats_view = {}
    monthStats_keyword = {}
    for m in logMonth:
        if "addreview" in m.values():
            monthStats_review[m['RequestContent']] = 1 + \
                monthStats_review.get(m['RequestContent'], 0)
        elif "searchbook" in m.values():
            monthStats_search[m['RequestContent']] = 1 + \
                monthStats_search.get(m['RequestContent'], 0)
        elif "viewbook" in m.values():
            monthStats_view[m['RequestContent']] = 1 + \
                monthStats_view.get(m['RequestContent'], 0)
        elif "searchkeyword" in m.values():
            monthStats_keyword[m['RequestContent']] = 1 + \
                monthStats_keyword.get(m['RequestContent'], 0)
    sort_value_review = sorted(monthStats_review.values())[::-1]
    top_x_review = []
    top_y_review = []
    for key in monthStats_review:
        if monthStats_review[key] in sort_value_review[0:10]:
            top_x_review.append(key)
            top_y_review.append(monthStats_review[key])

    sort_value_search = sorted(monthStats_search.values())[::-1]

    top_x_search = []
    top_y_search = []

    for keys in monthStats_search:

        if monthStats_search[keys] in sort_value_search[0:10]:
            top_x_search.append(keys)
            top_y_search.append(monthStats_search[keys])

    sort_value_view = sorted(monthStats_view.values())[::-1]
    top_x_view = []
    top_y_view = []

    for v in monthStats_view:

        if monthStats_view[v] in sort_value_view[0:10]:
            top_x_view.append(v)
            top_y_view.append(monthStats_view[v])

    sort_value_keyword = sorted(monthStats_keyword.values())[::-1]
    # print(sort_value_keyword)
    top_x_key = []
    top_y_key = []

    for k in monthStats_keyword:

        if monthStats_keyword[k] in sort_value_keyword[0:3]:
            top_x_key.append(k)
            top_y_key.append(monthStats_keyword[k])

    # print(top_x_search)
    return render_template("StatsPlot.html", top_x_review=top_x_review, top_y_review=top_y_review, top_x_search=top_x_search,
                           top_y_search=top_y_search, top_x_view=top_x_view, top_y_view=top_y_view,
                           top_x_key=top_x_key, top_y_key=top_y_key)


################review###############
def catch_reviews(asin):
    myresult = []
    try:
        cur = con.cursor()
        cur.execute("select reviewerName,summary,overall,helpful,reviewTime,reviewText from KindleReview where asin = %(asin)s;", {
                    'asin': asin})
        myresult = cur.fetchall()
        con.commit()

        print("Records for asin " + asin + " fetched from reviews table")
        print(myresult)
    except Error as error:
        print(error)
    return myresult


def insert_review(serialNum, asin, helpful, overall, reviewText, reviewTime, reviewID, reviewerName, summary, unixReviewTime):
    query1 = "insert into KindleReview(serialNum,asin,helpful,overall,reviewText,reviewTime,reviewID,reviewerName,summary,unixReviewTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        cur = con.cursor()
        cur.execute(query1, [serialNum, asin, helpful, overall, reviewText,
                             reviewTime, reviewID, reviewerName, summary, unixReviewTime])
        con.commit()
        print("Record inserted successfully into KindleReview table")

        print("MySQL connection is closed")
        return("Record inserted successfully into KindleReview table")
    except Error as error:
        print(error)


def get_last_id():
    try:
        cur = con.cursor()
        cur.execute('select max(serialNum) from KindleReview')
        last_id = cur.fetchone()
        con.commit()
        return last_id
    except Error as error:
        print(error)
