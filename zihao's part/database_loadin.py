import pandas as pd
from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

"""
This function is to load kindle review csv file into database app.db
"""

Base = declarative_base()

class cdb1(Base):
	
	#Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
	__tablename__ = 'Trial'
	__table_args__ = {'sqlite_autoincrement': True}
	
	#tell SQLAlchemy the name of column and its attributes:
	reviewID = Column(Integer, primary_key=True, nullable=False)
	asin = Column(Text)
	overall = Column(Integer)
	reviewText = Column(Text)
	reviewTime = Column(Text)
	reviewerID = Column(Text)
	reviewerName = Column(Text)
	summary = Column(Text)
	unixReviewTime = Column(Integer)

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
file_name = 'kindle_reviews.csv'
df = pd.read_csv(file_name)
df.to_sql(con=engine, index_label='id', name=cdb1.__tablename__, if_exists='replace')