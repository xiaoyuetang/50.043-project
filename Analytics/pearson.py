import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
import numpy as np

sc = SparkContext('local', 'testSpark')
spark = SparkSession(sc)

reviews = spark.read.csv('kindle_reviews.csv', header=True)
meta = spark.read.json('meta_Kindle_Store.json')

rText = reviews.select('asin','reviewText')

asin_avglength = rText.rdd.reduceByKey(lambda x,y:x+len(y))

price = meta.select('asin','price')

asin_avglength.show(10)

#
#asin_rText_price = rText.join(price).select('*')
#
#reviewLengths = asin_rText_price.select('reviewText').rdd.map(lambda x: len(x))
#
#asin_rText_price_len = asin_rText_price.join(reviewLengths).select('*')
#
#asin_rText_price_len.show(20)