import sys
import pandas as pd
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

sc = SparkContext('local', 'testSpark')
spark = SparkSession(sc)

reviews = spark.read.csv('kindle_reviews.csv', header=True)
meta = spark.read.json('meta_Kindle_Store.json')

df = pd.read_csv('kindle_reviews.csv')
df = df[['asin', 'reviewText']]
df['length'] = df['reviewText'].apply(lambda x: len(str(x)))
df = df.groupby('asin').mean()

asin_numbers = meta.select('asin').collect()
correlation = pd.DataFrame(columns=['asin', 'avg_length', 'price'])

count = 0
for i in asin_numbers:
	if count < 1000:
		asin = i['asin']
		try:
			length = df.loc[asin, : ][0]
			price = meta.where(col('asin') == asin).collect()[0]['price']
			print (asin, length, price)
			df2 = {"asin": asin, 'avg_length': length, 'price': price}
			correlation.append(df2, ignore_index=True)
		except:
			pass
		count += 1
	else:
		break