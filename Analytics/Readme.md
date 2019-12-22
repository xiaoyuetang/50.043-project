---Automation Script for EC2 launching of Hadoop and Spark---

Specify number of nodes to be created in line 132.
Have your account credentials ready via the AWS CLI, run aws configure.
AMI is now made public in the Singapore region/data centre.
Namenode and datanode IPs can be obtained from python console.

note: memory limitations/errors result in pearson/tfidf not being able to run on these instances, as pyspark refuses to install. Please use the preconfigured server (same settings, just with successful manual pyspark installation) to test the functions.

---SSH into Namenode---
cd to Analytics folder and use the following ssh command
ssh -i "ksdbkey.pem" ubuntu@ec2-54-208-153-234.compute-1.amazonaws.com

---Inside Namenode---
Directories 'hadoop' and 'spark' are in home dir (~).

Start hadoop: 
start-dfs.sh

Start spark:
~/spark/sbin/start-all.sh

---Analytics portion---
For this portion, we cd to the analytics folder, where the .py scripts are located

cd ~/50.043-project/Analytics 

Correlation:
	python3 pearson.py
	// result will be printed in console

TF-IDF:
	python3 tfidf1.py
	python3 tfidf2.py
	// result will be written to a file called 'tfidf'

Number of nodes: 
  Without automation script:
    The defualt number of nodes is 4. If you want to run on 2 nodes, then you can manually turn off 2 machines and the run on     2 out of 4 nodes.
