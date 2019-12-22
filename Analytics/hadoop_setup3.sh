# ./hadoop_setup.sh ip0 ip1 ip2
sudo apt-get install python3-mysql.connector

set -e
if [ "$#" -lt 1 ]
then
echo  "Please insert at least one argument"
exit
else
echo -e "\c"
fi

> ~/spark/conf/slaves
> ~/hadoop/etc/hadoop/workers

echo "$#" >> ~/readings.txt
echo "$1" >> ~/readings.txt
echo "setting namenode $1 in core-site.." > ~/readings.txt
sudo sed -i "s/(NAMDENODEIP)/$1/g" ~/hadoop/etc/hadoop/core-site.xml
echo "setting namenode in mapred-site.." >> ~/readings.txt
sudo sed -i "s/(NAMENODEIP)/$1/g" ~/hadoop/etc/hadoop/mapred-site.xml
echo "setting namenode in yarn-site.." >> ~/readings.txt	
sudo sed -i "s/(NAMENODEIP)/$1/g" ~/hadoop/etc/hadoop/yarn-site.xml;
echo "setting namenode in masters.." >> ~/readings.txt
sudo sed -i "s/(NAMENODEIP)/$1/g" ~/hadoop/etc/hadoop/masters;



if [ $# > 1 ];
then
	echo "namenode operations" >> ~/readings.txt
	for ((i=2; i<=$#; ++i));
	do
		echo "setting worker "${!i}" in workers.." >> ~/readings.txt
		echo "${!i}">> ~/hadoop/etc/hadoop/workers;
		echo "setting worker in slaves.." >> ~/readings.txt
		echo "${!i}">> ~/spark/conf/slaves
	done
	echo "initialising hdfs and spark on namenode...">> ~/readings.txt
	hdfs namenode -format
	./start_hdfs_spark.sh
	hdfs dfs -mkdir /datasets
	cd ~/50.043-project/Analytics/
	yes Y | hdfs dfs -put kindle_reviews.csv meta_Kindle_Store.json /datasets
	echo "done, setup complete" >> ~/readings.txt
fi
