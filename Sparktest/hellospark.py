from pyspark.sql import SparkSession

sparkSession = SparkSession.builder.appName("testSpark").getOrCreate()

df_load = sparkSession.read.csv('hdfs://localhost:9000')
df_load.show()
