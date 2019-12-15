# import boto3
# import botocore
# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all():
#     print(bucket.name)
# data = open('/Users/hehe/Desktop/ggdd/WechatIMG11909.jpeg', 'rb')
# s3.Bucket('kindlemetadata').put_object(Key='test.jpg', Body=data)

import boto3
import time
import subprocess
import botocore
import paramiko
import os

## Global variable to access EC2 functions provided by Boto3;

ec2 = boto3.resource('ec2')
# response = ec2.describe_vpcs()
# vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '') #Get VPC id of this aws account
# print(vpc_id)

###########################

def create_new_webserver_instance(security_group_id, key_name,numofinstances):
    '''
        Creates and configures a AWS EC2 t2.micro instance with a pre-configured nginx
        web server.
        Requires a single Security Group Id from the user's AWS account and a SSH private
        pem key located in the same directory as this file as arguments to be used by
        the instance.
    '''
    print('Creating a new web server instance using the ' + key_name + ' key and ' + security_group_id + ' security group..')

    try:
        new_instance = ec2.create_instances(
            ImageId = 'ami-069116f0fd840fa20',
            MinCount = 1,
            MaxCount = numofinstances,
            InstanceType = 't2.micro',

            ## Security group the instance will abide to (must be in your AWS account);
            SecurityGroupIds = [security_group_id],

            ## Name of private key to be used to launch the instance (should be in the same directory as this file);
            KeyName = key_name,
        )

        print('New instance created (ID: ' + new_instance[0].id + ').')


        return new_instance

    except Exception as error:
        print('An error occured while trying to create a new instance: ' + error)

def execute_commands_in_instance_mongodb(public_ip_address,key_name):
    key = paramiko.RSAKey.from_private_key_file(key_name+'.pem')

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    instance_ip=public_ip_address
    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/setup_mongo.sh'
    cmd2='chmod +x setup_mongo.sh'
    cmd3='sh setup_mongo.sh'

    try:

        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance

        stdin, stdout, stderr = client.exec_command(cmd1)

        print(stdout.channel.recv_exit_status() )
        stdin, stdout, stderr = client.exec_command(cmd2)

        print(stdout.channel.recv_exit_status() )
        stdin, stdout, stderr = client.exec_command(cmd3)

        print(stdout.channel.recv_exit_status() )

        # close the client connection once the job is done

        client.close()

    except Exception as e:

        print (e)
def execute_commands_in_instance_mysql(public_ip_address,key_name):
    key = paramiko.RSAKey.from_private_key_file(key_name+'.pem')

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    instance_ip=public_ip_address
    #commands
    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/setup_mysql_new.sh'
    cmd2='chmod +x setup_mysql_new.sh'
    cmd3='sh setup_mysql_new.sh'
    cmd4='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/setup_tables.sh'
    cmd5='chmod +x setup_tables.sh'
    cmd6='sh setup_tables.sh'
    cmds=[cmd1,cmd2,cmd3,cm4,cm5,cm6]



    try:

        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.channel.recv_exit_status() )
        # close the client connection once the job is done

        client.close()

    except Exception as e:

        print (e)

def execute_commands_in_instance_mongoLog(public_ip_address,key_name):
    key = paramiko.RSAKey.from_private_key_file(key_name+'.pem')

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    instance_ip=public_ip_address
    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/setup_mongoLog.sh'
    cmd2='chmod +x setup_mongo.sh'
    cmd3='sh setup_mongo.sh'

    try:

        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance

        stdin, stdout, stderr = client.exec_command(cmd1)

        print(stdout.channel.recv_exit_status() )
        stdin, stdout, stderr = client.exec_command(cmd2)

        print(stdout.channel.recv_exit_status() )
        stdin, stdout, stderr = client.exec_command(cmd3)

        print(stdout.channel.recv_exit_status() )

        # close the client connection once the job is done

        client.close()

    except Exception as e:

        print (e)

def execute_commands_in_instance_server(public_ip_address,key_name,iplist):
    key = paramiko.RSAKey.from_private_key_file(key_name+'.pem')

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    instance_ip=public_ip_address
    cmd8="python -c 'import os;os.environ['mysql_ip']="+iplist[0]+";os.environ['mongod_ip']="+iplist[1]+";os.environ['logmongod_ip']="+iplist[3]+"'"
    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/pipinstalllibs.sh'
    cmd2='chmod +x pipinstalllibs.sh'
    cmd3='sh pipinstalllibs.sh'
    text='server {\n  isten 80;\n  listen [::]:80 ipv6only=on default_server;\n  server_name '+public_ip_address+';\n  location / {\n    proxy_pass http://127.0.0.1:8000;\n  }\n}'
    cmd4="echo -e '"+text+"'| sudo tee /etc/nginx/sites-enabled/flaskapp"
    cmd5='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/flask_setup.sh'
    cmd6='chmod +x flask_setup.sh'
    cmd7='sh flask_setup.sh'
    cmds=[cmd8,cmd1,cmd2,cmd3,cmd4,cmd5,cmd6,cmd7]


    try:

        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.channel.recv_exit_status() )
        # close the client connection once the job is done

        client.close()

    except Exception as e:

        print (e)

def main():

    print('This python module will create a AWS EC2 web server instance and execute a web server monitoring script.')

    security_group_id = 'sg-04db4aa07b4b2d47d'

    key_name = 'hello'
    numofinstances=4
    client = boto3.client('ssm')




    # #create intsance for sql
    # instance = create_new_webserver_instance(security_group_id, key_name,numofinstances)
    # iplist=[]
    # for i in range(numofinstances):
    #     iplist.append(instance[i].public_ip_address)


    # print('Sleeping the program for 60 seconds to let the instance to be configured..')
    # time.sleep(60)
    # instance[0].reload()

    # execute_commands_in_instance_mysql(iplist[0],key_name)

    # print('sql setup done')

    #instance[1].reload()
    # execute_commands_in_instance_mongodb(iplist[1],key_name)
    # print('mongodb setup done')

    #instance[2].reload()
    # execute_commands_in_instance_mongoLog(iplist[2],key_name)
    # print('mongodb log setup done')


    # instance[3].reload()
    # execute_commands_in_instance_server(iplist[3],key_name,iplist)

    # print('server setup done')


if __name__ == '__main__':
  main()

# exists = True
# try:
#     s3.meta.client.head_bucket(Bucket='mybucket')
# except botocore.exceptions.ClientError as e:
#     # If a client error is thrown, then check that it was a 404 error.
#     # If it was a 404 error, then the bucket does not exist.
#     error_code = e.response['Error']['Code']
#     if error_code == '404':
#         exists = False
