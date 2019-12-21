hdfs namenode -format
start-dfs.sh
~/spark/sbin/start-all.sh
hdfs dfs -mkdir /datasets
cd ~/50.043-project/Analytics/
hdfs dfs -put kindle_reviews.csv meta_Kindle_Store.json /datasets
