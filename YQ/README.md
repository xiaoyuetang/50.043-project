### Run program

Go inside the Zihao's Part folder, run in terminal:

` $ source venv/bin/activate`

` (venv) $ export FLASK_APP=50043-project.py`

` (venv) $ flask run`

To activate the debug mode, run in terminal:

` (venv) $ export FLASK_DEBUG=1 ` 

You would see this
* Serving Flask app "50043-project"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

If required login, please use username: susan, password: cat

+ For adding a new book, you could click the widget called "Add a bock" or you could also use http://127.0.0.1:5000/addbook
+ For adding a new review, you could find in the bottom of page http://127.0.0.1:5000/book_review or use http://127.0.0.1:5000/addreview


### Database Query

Go inside the Zihao's Part folder, run python terminal

Once in the Python prompt, let's import the database instance and the models:

` from app import db`

` from app.models import User, Post, Trial`

Start by creating a new user:

` u = User(username='john', email='john@example.com')`

` db.session.add(u)`

` db.session.commit()`

Basic Queries:

` users = User.query.all()`
