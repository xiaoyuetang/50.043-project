# ISTD 50.043 Book Review

In this project, we have built a web application for Kindle book reviews, one that is similar to Goodreads. We have started with some public datasets from Amazon, and design and implement your application around them.

## Getting Started

Demo: http://54.185.13.103/

If you want to recreate by you own, follow the steps under **Automation Script**



### Prerequisites

What things you need to install

```
flask
flask_sqlalchemy
flask_migrate
flask_login
flask_pymongo
mysql-connector-python
mysql-connector-python-dd
mysql-connector-python-rf
flask_mysqldb
flask_wtf
boto3
botocore
```

### Automation Scripts

Automate creating instances and host database aw well as the app itself on EC2

Clone or download a copy here and follow the steps:
1. Get an Amazon Web Service account at https://aws.amazon.com, record down your **Access Key ID** and **Secret Access Key**
2. Run automation script to get server up
In your terminal/cml
```
cd /50.043-project/automation\ script
python autoScriptForFrontEnd.py
```
![cml demo](screenshot/automation1.png)

！in case the security group in your account doesn't fullfil all the requirements then you can type in any name you want as your security group name, in the automation script, it will help you create a security group using the name you provided.

! same for key name, you'd better use the key in the same folder as the automation script, if cannot find any keys in the same folder, then just type any name for the key, the script will help you to create one.
3. Go to the IP address printed in the console to view the app


End with an example of getting some data out of the system or using it for a little demo

## Run it locally

Clone or download a copy here and follow the steps:
```
cd /50.043-project/flaskappDemo
python 50043-project.py
```
In your terminal/cml then go to 0.0.0.0

## Analytics System

All the related scripts as well as README are all in Analytics folder : [https://github.com/yqyqyq123/50.043-project/Analytics]

## Screenshots
### Home page
![app demo](screenshot/app-screenshot1.png)

### Plots for stastics
![app demo](screenshot/app-screenshot7.png)

### User/Admin edit profile
![app demo](screenshot/app-screenshot8.png)

### Add a new book (for admin only)
![app demo](screenshot/app-screenshot2.png)

### Contact (Admin side)
![app demo](screenshot/app-screenshot3.png)

### Contact (User side)
![app demo](screenshot/app-screenshot4.png)

### History page:
![app demo](screenshot/app-screenshot5.png)

### System history (for admin only)
![app demo](screenshot/app-screenshot6.png)


## Built With

* [Bootstrap](https://getbootstrap.com/) - The CSS web framework used
* [Flask](https://maven.apache.org/) - Micro web framework written in Python
* [AWS](https://aws.amazon.com) - Amazon Web Service


## Authors
* Gou Yuanyuan 1002972
* Li Yueqin 
* Li Zihao 1002966
* Tang Xiaoyue 1002968
* Ng Jen Yang 1003007
* Khai Sheen


