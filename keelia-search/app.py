from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, SelectField

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    search_input = None
    if request.method == 'POST' and request.form['search-btn'] == 'Search':
        search_input = request.form['search-input']
        return redirect(url_for('search', search_input=search_input))
    return render_template('index.html')


@app.route('/search-result')
def search():
    search_input = request.args['search_input']
    return render_template('search-result.html', search_input=search_input)


if __name__ == '__main__':
    app.run(debug=True)
