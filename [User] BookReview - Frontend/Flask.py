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
    b1 = "Harry Potter"
    c1 = "https://img1-placeit-net.s3-accelerate.amazonaws.com/uploads/stage/stage_image/39885/large_thumb_book-cover-horror-novel-527.jpg"
    b2 = "Rich Dad Poor Dad"
    b3 = "Lord of The Rings"
    return render_template("history.html", book1=b1, book2=b2, book3=b3,
                           cover1=c1)


if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Something wrong")
