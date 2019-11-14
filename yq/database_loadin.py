import pandas as pd
from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

'''
Load the csv file into SQL database
'''

Base = declarative_base()

class reviewerInformation(Base):
	__tablename__ = 'reviewer_information'
	__table_args__ = {'sqlite_autoincrement': True}
	
	reviewerID = Column(Text, primary_key=True, nullable=False)
	reviewerName = Column(Text)

class review(Base):
	__tablename__ = 'review'
	__table_args__ = {'sqlite_autoincrement': False}
	
	reviewID = Column(Integer, primary_key=True, nullable=False)
	overall = Column(Integer)
	reviewText = Column(Text)
	summary = Column(Text)
	unixReviewTime = Column(Integer)
	
	# not inlcuded helpful[0] and helpful[1]

class reviewerReviews(Base):
	__tablename__ = 'reviewer_reviews'
	__table_args__ = {'sqlite_autoincrement': False}
	
	reviewID = Column(Integer, primary_key=True, nullable=False)
	asin = Column(Text)
	reviewerID = Column(Text)
	
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
file_name = 'kindle_reviews.csv'

df = pd.read_csv(file_name)
table1_col = ['reviewerID', 'reviewerName']
table2_col = ['reviewID', 'overall', 'reviewText', 'summary', 'unixReviewTime']
table3_col = ['reviewID', 'asin', 'reviewerID']
df1 = df[table1_col]
df2 = df[table2_col]
df3 = df[table3_col]

df1.to_sql(con=engine, index_label='id', name=reviewerInformation.__tablename__, if_exists='replace')
df2.to_sql(con=engine, index_label='id', name=review.__tablename__, if_exists='replace')
df3.to_sql(con=engine, index_label='id', name=reviewerReviews.__tablename__, if_exists='replace')