from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sheen")
def sheen():
    return "<h1>COOL</h1> guy!!!"

@app.route("/review")
def review():
    return render_template("review-page.html")
    
if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Something wrong")
    