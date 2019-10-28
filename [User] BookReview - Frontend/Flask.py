from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/form")
def form():
    return render_template("randomForm.html")


@app.route("/form", methods=['POST'])
def get_name():
    name = request.form['name']
    print("This idiot's name is", name)
    return render_template("randomForm.html")


@app.route("/review")
def review():
    return render_template("review-page.html")


@app.route("/review", methods=["POST"])
def submit_review():
    desc = request.form['reviewDesc']
    review = request.form['reviewTextInput']
    return "<strong>" + desc + "</strong>" + review


@app.route("/history")
def login():
    ''' 
    Using dummy data for now. Fetch from DB next time.
    '''
    b1 = "Harry Potter"
    c1 = "https://img1-placeit-net.s3-accelerate.amazonaws.com/uploads/stage/stage_image/39885/large_thumb_book-cover-horror-novel-527.jpg"
    a1 = "A. Dinh"
    tags1 = ["Art", "Cookbooks"]

    b2 = "Rich Dad Poor Dad"
    c2 = "https://img2-placeit-net.s3-accelerate.amazonaws.com/uploads/stage/stage_image/37837/large_thumb_stage.jpg"
    a2 = "B. Dinh"
    tags2 = ["Self Help", "Thriller", "Graphic Novels"]

    b3 = "Lord of The Rings"
    c3 = "https://i.pinimg.com/236x/82/79/74/827974d98ed5dabfbeecbdae890caebf.jpg"
    a3 = "C. Dinh"
    tags3 = ["Business", "Fiction", "Nonfiction"]

    books = [b1, b2, b3]
    covers = [c1, c2, c3]
    author = [a1, a2, a3]
    tags = [tags1, tags2, tags3]

    return render_template("history.html", count=len(books), books=books, covers=covers, author=author, tags=tags)


if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Something wrong")
