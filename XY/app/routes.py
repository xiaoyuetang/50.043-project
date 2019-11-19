from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, ReviewForm, RegistrationForm
from app import db, log
from app.models import User, Trial, Review, ReviewerReviews, ReviewerInformation, Book
from werkzeug.urls import url_parse
from datetime import datetime, date


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
        review = Trial(reviewID=reviewID, overall=overall,
                       reviewText=reviewText)
        db.session.add(review)
        db.session.commit()

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('add_review.html', title='Add a Review', form=form)

####################### below are revisited version ########################

# main page
# html file: index.html
# 我把左上角的logo暂定为点了以后进到某个书的 review page
@app.route('/')
@app.route('/index')
def index():
    dive = Book(title='Flipped', year=2000)
    dive.save()
    return render_template('index.html')

# need to combine with 猫姐姐's Login Form
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        # print(request.form['loginbutton'])
        # print(request.form['loginbutton'] == 'Log In')
        if request.form['loginbutton'] == 'Log In':
            print(request.form)
            userid = request.form['userid']
            password = request.form['password']
            print(userid)
            print(password)

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
        else:
            pass  # unknown
    # elif request.method == 'GET':
    #     pass
    return render_template('login.html')

    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('index')
    #     return redirect(next_page)
    # return render_template('login.html', title='Sign In', form=form)

# 这边猫姐姐需要在login的基础上, 加一个logout的选项
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# need to combine with 猫姐姐's Signup Form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

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


# 看到书的 Description / 可以 write a review
@app.route("/review", methods=["POST", "GET"])
def review():
    '''
    Get the header and review from review form and do something upon submit
    '''
    x = Trial.query.filter_by(reviewID=10).all()
    print(x)
    form = request.form
    if request.method == "POST":
        if 'reviewbutton' in form:
            id = 000000  # NEED HELP HERE
            reviewID = 0  # NEED HELP HERE
            asin = 0000  # NEED TO GET FROM KINDLE METADATA DB
            overall = form['overall'].count("\u2605")  # count number of stars
            reviewText = form['reviewText']
            reviewTime = get_review_time()
            reviewerID = "A29cDXC"  # NEED TO GET FROM DB
            reviewerName = "ASDADS"  # NEED TO GET FROM DB
            summary = form['summary']
            unixReviewTime = int(datetime.utcnow().timestamp())
            review = Trial(reviewID=reviewID, asin=asin, overall=overall,
                           reviewText=reviewText, reviewTime=reviewTime, reviewerID=reviewerID,
                           reviewerName=reviewerName, summary=summary, unixReviewTime=unixReviewTime)
            # db.session.add(review)
            # db.session.commit()
            print(review)

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            pass  # something else

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
    # 格式是这样但是Book的metadata gyy还没弄好
    # new_book = Book(title='Flipped', year=2000)
    # new_book.save()
    print(ClientEmail)

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
@login_required
def profile():
    return render_template("profile.html")


def get_review_time():
    today = date.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)

    return month + " " + day + ", " + year
