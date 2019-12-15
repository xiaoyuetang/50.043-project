import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import *
from pyspark.sql import SparkSession

sc = SparkContext('local', 'testSpark')
spark = SparkSession(sc)

reviews = spark.read.csv('kindle_reviews.csv', header=True)
meta = spark.read.json('meta_Kindle_Store.json')

print(reviews.schema)
print(meta.schema)

print(reviews)
reviews.show(5)
