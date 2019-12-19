import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as fns

hdfs_addr="hdfs://ec2-54-162-120-120.compute-1.amazonaws.com:9000/user/ubuntu"

sc = pyspark.SparkContext("spark://ec2-54-162-120-120.compute-1.amazonaws.com:7077", "Correlation")
spark = SparkSession(sc)

reviews = spark.read.csv(f"{hdfs_addr}/datasets/kindle_reviews.csv", header=True)
asinr = reviews.select('asin','reviewText')
asinrl = asinr.withColumn('reviewLength',fns.length('reviewText'))
meta = spark.read.json(f"{hdfs_addr}/datasets/meta_Kindle_Store.json")

asin_avgl = asinrl.groupBy('asin').avg('reviewLength')

asin_avgl.take(5)