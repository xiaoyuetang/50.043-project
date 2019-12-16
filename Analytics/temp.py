import mysql.connector as sqldb
quit()
import mysql.connector as sqldb
quit()
import mysql.connector as sqldb
quit(0
quit()
import pyspark
sc = pyspark.SparkContext("3.85.48.139", "pearsy")
sc = pyspark.SparkContext("ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
sc = pyspark.SparkContext("https://ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
sc = pyspark.SparkContext("hdfs://ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
exit()
import pyspark
sc = pyspark.SparkContext("ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
sc = pyspark.SparkContext("https://ec2-3-85-48-139.compute-1.amazonaws.com", "pearsy")
exit()
import pyspark
sc = pyspark.SparkContext("sparkL//ip-172-31-39-43.ect.internal:7077", "pearsy")
sc = pyspark.SparkContext("spark://ip-172-31-39-43.ect.internal:7077", "pearsy")
sc = pyspark.SparkContext("https://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc = pyspark.SparkContext("ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc = pyspark.SparkContext("spark:nnode:7077", "pearsy")
print(sc)
del sc
sc = pyspark.SparkContext("spark:nnode:7077", "pearsy")
sc
print(sc)
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy").getOrCreate()
exit()
import pyspark
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7070", "pearsy")
sc
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7070", "pearsy")
sc
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7070", "pearsy")
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc
print("hello")
from pyspark.sql import SparkSession
spark = SparkSession(sc)
reviews = spark.read_csv("kindle_reviews.csv")
reviews = spark.read.csv("kindle_reviews.csv")
reviews = spark.read.load("kindle_reviews.csv", format="csv")
exit
sc
spark
sc.stop()
sc
sc = SparkContext("spark://ec2-3-85-48-139-compute-1.amazonaws.com:7077", "pearsy")
import pyspark
sc = pyspark.SparkContext("spark://ec2-3-85-48-compute-1.amazonaws.com:7077", "pearsy")
sc = pyspark.SparkContext("spark://ec2-3-85-48-139-compute-1.amazonaws.com:7077", "pearsy")
sc
sc = pyspark.SparkContext("spark://ec2-3-85-48-139-compute-1.amazonaws.com:7077", "pearsy")
print(sc)
sc
import pyspark
sc = pyspark.SparkContext("spark://ec2-3-85-48-139.compute-1.amazonaws.com:7077", "pearsy")
sc
from pyspark.sql import SparkSession
spark = SparkSession(sc)
reviews = spark.read.csv("kindle_reviews.csv")
reviews = spark.read.csv("./kindle_reviews.csv")
reviews = spark.read.csv("~/50.043-project/Analytics/kindle_reviews.csv")
reviews = spark.read.csv("~0.043-project/Analytics/kindle_reviews.csv")
import pyspark
from pyspark.sql import SparkSession
sc = pyspark.SparkContext("spark://3.93.14.131:7077", "test")
exec(testspark.py)
exec("testspark.py")
execfile("./testspark.py")
exec("./testspark.py")
exec(open("./testspark.py").read())
exec(open("testspark.py").read())
sc
text = sc.textfile("alice.txt")
text = sc.textFile("alice.txt")
df = text.map(lambda x: x.split(' ')).toDF()
df
text
text.show()
text.take(10)
exec(open("testspark.py").read())
import pyspark.sql.functions as fns
reviews = spark.read.csv("hdfs://3-93-14-131:9000", header=True)
reviews = spark.read.csv("hdfs://ec2-3-93-14-131.compute-1.amazonaws.com:9000", header=True)
reviews = spark.read.csv("hdfs://ec2-3-93-14-131.compute-1.amazonaws.com:9000/user/ubuntu/kindle/kindle_reviews.csv", header=True)
asinr = reviews.select('asin','reviewText')
asinr.take(1)
asinrl = asinr.select('asin', fns.length('reviewText')).join(asinr)
asinrl.take(1)
asinrl.schema
asinr.schema
asinrl = asinr.withColumn('reviewLength',fns.length('reviewText'))
asinrl.take(1)
lol
import readline
readline.write_history_file('./pearson.py')
ls
exec(open('pearson.py').read())
dir()
hdfs_addr="hdfs://ec2-3-93-14-131:9000"
hdfs_addr="hdfs://ec2-3-93-14-131:9000/user/ubuntu"
meta = spark.read.json(f"{hdfs_addr}/datasets/meta_Kindle_Store.json")
hdfs_addr="hdfs://ec2-3-93-14-131.compute-1.amazonaws.com:9000/user/ubuntu"
meta = spark.read.json(f"{hdfs_addr}/datasets/meta_Kindle_Store.json")
meta.schema
import readline
readline.write_history_file(
readline.write_history_file('./temp.py')
