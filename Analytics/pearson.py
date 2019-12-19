import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as fns

hdfs_addr="hdfs://ec2-54-208-153-234.compute-1.amazonaws.com:9000"

 sc = pyspark.SparkContext("spark://ec2-54-208-153-234.compute-1.amazonaws.com:7077", "Correlation")
#sc = pyspark.SparkContext("local", "Correlation")
spark = SparkSession(sc)

reviews = spark.read.csv(f"{hdfs_addr}/datasets/kindle_reviews.csv", header=True)
#reviews = spark.read.csv(f"kindle_reviews.csv", header=True)
asinr = reviews.select('asin','reviewText')
asinrl = asinr.withColumn('reviewLength',fns.length('reviewText'))

meta = spark.read.json(f"{hdfs_addr}/datasets/meta_Kindle_Store.json")
#meta = spark.read.json("meta_Kindle_Store.json")

# asin_avgl = asinrl.groupBy('asin').avg('reviewLength')
asin_avgl = asinrl.groupBy('asin').avg('reviewLength')

#asin_avgl.take(5)

# join asin_avgl and meta with column asin
table = asin_avgl.join(meta.select('asin', 'price'), ['asin'])

# return Column for the Pearson Correlation Coefficient 
table = table.agg(fns.corr('avg(reviewLength)', "price").alias('pearson_correlation'))

table.select("pearson_correlation").show()