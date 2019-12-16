import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as fns

hdfs_addr="hdfs://ec2-3-93-14-131.compute-1.amazonaws.com:9000/user/ubuntu"

sc = pyspark.SparkContext("spark://ec2-3-93-14-131.compute-1.amazonaws.com:7077", "Correlation")
spark = SparkSession(sc)

reviews = spark.read.csv("hdfs://ec2-3-93-14-131.compute-1.amazonaws.com:9000/user/ubuntu/kindle/kindle_reviews.csv", header=True)
asinr = reviews.select('asin','reviewText')
asinrl = asinr.withColumn('reviewLength',fns.length('reviewText'))
meta = spark.read.json(f"{hdfs_addr}/datasets/meta_Kindle_Store.json")
