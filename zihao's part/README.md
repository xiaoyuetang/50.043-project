### Run program

Go inside the Zihao's Part folder, run in terminal:

`$ source venv/bin/activate`
`(venv) $ export FLASK_APP=50043-project.py`
`(venv) $ flask run`

To activate the debug mode, run in terminal:

`(venv) $ export FLASK_DEBUG=1`

You would see this
* Serving Flask app "50043-project"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

If required login, please use username: susan, password: cat


### Database Query
Go inside the Zihao's Part folder, run python terminal

Once in the Python prompt, let's import the database instance and the models:

`from app import db`
`from app.models import Review`

Start by creating a new review:

`review = Review(col_name1= , col_name2= )`
`db.session.add(review)`
`db.session.commit()`

Basic Queries:

`users = User.query.all()`

### Database Migrate

Once the database configuration has been changed (models.py modified)

Run in terminal, 
`flask db migrate -m "comments"`
`flask db upgrade`