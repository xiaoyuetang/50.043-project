## Run program

1. In terminal, run
$ source venv/bin/activate
(venv) $ export FLASK_APP=50043-project.py
(venv) $ flask run

You would see this: xxx running on http://127.0.0.1:5000/
to view the book review page, use http://127.0.0.1:5000/bookreviews


## Use database

1. Once in the Python prompt, let's import the database instance and the models:

>>> from app import db
>>> from app.models import User, Post

2. Start by creating a new user:

u = User(username='john', email='john@example.com')
>>> db.session.add(u)
>>> db.session.commit()

3. 

users = User.query.all()
>>> users
[<User john>, <User susan>]
>>> for u in users:
...     print(u.id, u.username)
...
1 john
2 susan