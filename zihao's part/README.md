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

### Add new records
```
# add a new record
user_obj = User(name="susan", passwd="cat")
db.session.add(user_obj)
db.session.commit()

# add multiple records
user_obj1 = User(name="susan1", passwd="cat1")
user_obj2 = User(name="susan2", passwd="cat2")
db.session.add_all([user_obj1,user_obj2])
db.session.commit()
```

### Query
```
# get the first object that matches
data = User.query.filter_by(name='susan').first()

# get all objects that match
data = User.query.filter_by(name='susan').all()

# output data
print (data[0].name)

# no query condition
data = User.query.filter_by().all()

# get all data with selected columns
data = User.query(User.col1, User.col2, User.col3).all()

# multiple conditions
data = User.query.filter(condition1).filter(condition2).all()

# 模糊查询
data = User.query.filter(User.name.like('J%')).all()

# and & or
from sqlalchemy import and_, or_
data = User.query.filter(and_(User.id > 2, User.name.like('J%'))).all()
data = User.query.filter(or_(User.id > 2, User.name.like('J%'))).all()

# in_
data = Session.query(User).filter(User.id.in_([1,3])).all()
data = Session.query(User).filter(User.name.in_(['susan', 'susan1'])).all()

# query in order
data = User.query.order_by(User.name.desc()).all()
```

### Modify data
```
# 1.1 Assign
data = User.query.filter_by(name='Marry').first()
data.name = 'Tom'
db.session.commit()

# 1.2 Update
User.session.query.filter_by(name='Tom').update({'name': 'Hary'})
Session.commit()

# Rollback
User.ession.query.filter_by(name='Hary').update({'name': 'John'})
session.rollback()
Session.commit()
```

### 统计
```
data = User.query.filter(User.name.like('%a%')).count()
```

### Group 
```
from sqlalchemy import func

data = Session.query(User.name, func.count(User.name)).group_by(User.name).all()
```
