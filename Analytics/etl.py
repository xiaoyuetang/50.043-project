import mysql.connector as sqldb
import os
import csv

OUTFILE = "out"
DATABASE = "flaskproject"
ec2host = 'ec2-34-220-172-38.us-west-2.compute.amazonaws.com'
# ec2host='54.189.148.212'
con = sqldb.connect(host=ec2host, user="root", passwd="", db=DATABASE)


with open(f"{OUTFILE}", mode="w") as f:
    cur = con.cursor()
    cur.execute(
        "select distinct asin from KindleReview where overall=5 limit 27")
    data = cur.fetchall()
    result = []
    for i in data:
       f.write(f'{i[0]}\n')
    con.commit()


os.system(f'hdfs dfs -put -f {OUTFILE} test')
os.system(f'rm {OUTFILE}')
