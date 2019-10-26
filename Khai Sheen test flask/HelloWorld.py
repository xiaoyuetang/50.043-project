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


if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Something wrong")
