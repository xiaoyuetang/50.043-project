import mysql.connector as sqldb

# save datas from MySQL database to txt file

DATABASE="flaskproject"
ec2host='ec2-34-220-172-38.us-west-2.compute.amazonaws.com'
# ec2host='54.189.148.212'
con= sqldb.connect(host=ec2host, user="root", passwd="", db=DATABASE)

cur = con.cursor()
cur.execute("select asin, reviewText from KindleReview")
data = cur.fetchall()

result =[]
with open('reviews.txt', 'a') as f:
	for i in data:
		line = str(i[1])
		f.write(line)
		f.write('\n')
		# result.append(i[1])
con.commit()

# print (result)