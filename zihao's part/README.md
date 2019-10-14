## Run program

1. In terminal, run
<p>$ source venv/bin/activate </p>
<p>(venv) $ export FLASK_APP=50043-project.py </p>
<p>(venv) $ flask run </p>



You would see this: xxx running on http://127.0.0.1:5000/
To view the book review page, use http://127.0.0.1:5000/bookreviews


## Use database

1. Once in the Python prompt, let's import the database instance and the models:

<p>>>> from app import db </p>
<p>>>> from app.models import User, Post </p>

2. Start by creating a new user:

<p> u = User(username='john', email='john@example.com') </p>
<p> >>> db.session.add(u) </p>
<p> >>> db.session.commit() </p>

3. 

<p>users = User.query.all() </p>
<p>>>> users </p>
<p>[<User john>, <User susan>] </p>
<p>>>> for u in users: </p>
<p>...     print(u.id, u.username) </p>
<p>... </p>
<p>1 john </p>
<p>2 susan </p>
