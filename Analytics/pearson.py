import sys
import pyspark
from pyspark import *

sc = SparkContext('local', 'testSpark')
spark = SparkSession(sc)

reviews = spark.read.csv('kindle_reviews.csv', header=True)
meta = spark.read.json('meta_Kindle_Store.json')

rText = reviews.select('asin','reviewText')

price = meta.select('asin','price')

asin_rText_price = rText.join(price).select('*')

reviewLengths = asin_rText_price.select('reviewText').map(lambda x: len(x))

