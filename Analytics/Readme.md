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

