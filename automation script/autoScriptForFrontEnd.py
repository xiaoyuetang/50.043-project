import boto3
import time
import subprocess
import botocore
import paramiko
import os
import pprint as pp
from botocore.exceptions import ClientError

## Global variable to access EC2 functions provided by Boto3;

key = input("Please enter your aws access key:\n")
secret_key = input("Please enter your aws secret access key:\n")
# key='AKIAJCRZFPQYZG2BF36A'
# secret_key='oHCBX5PzEOyXYpdAmjgoiwnucFnEDMYCYVEYjZQu'
region_name = 'us-west-2'
ec2 = boto3.resource('ec2',
    aws_access_key_id=key,
    aws_secret_access_key=secret_key,
    region_name=region_name)
# ec2 = boto3.resource('ec2',)
ec2_client = boto3.client('ec2',
    aws_access_key_id=key,
    aws_secret_access_key=secret_key,
    region_name=region_name)

###########################
#Function for creating security group
def create_security_group(security_group_name):

    response = ec2_client.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '') #Get VPC id of this aws account

    try:
        response = ec2_client.create_security_group(GroupName=security_group_name,
                                             Description="This is for create security group",
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        pp.pprint('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,      ## SSH
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 27017,   ## MongoDB
                 'ToPort': 27017,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 3306,    ## mySQL
                 'ToPort': 3306,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}

            ])
        pp.pprint('Ingress Successfully Set %s' % data)

    except ClientError as e:
        pp.pprint(e)

def create_new_webserver_instance(security_group_name, key_name,numofinstances):
    '''
        Creates and configures a AWS EC2 t2.micro instance with a pre-configured nginx
        web server.
        Requires a single Security Group Id from the user's AWS account and a SSH private
        pem key located in the same directory as this file as arguments to be used by
        the instance.
    '''
        # Connection

    #Check if our security group exists,otherwise create one

    try:
        response = ec2_client.describe_security_groups(GroupNames=[security_group_name])
        print("Security group: {} exits".format(security_group_name))
    #     pp.pprint(response)
    except ClientError as e:
    #     pp.pprint(e)
        print("This security group doesn't exist,creating a new one...\n")
        create_security_group(security_group_name)


    #Check if our key-pair exists,otherwise create one
    key_not_exist = True

    keyPairs = ec2_client.describe_key_pairs()
    for key in keyPairs.get('KeyPairs'):
        if key.get('KeyName') == key_name:
            key_not_exist = False
            print("key-pair: {} exists.".format(key_name))
            break
    if key_not_exist :
        print("Generating a unique key for EC2 instances")
        generate_key_pairs(key_name)
    print('Creating a new web server instance using the ' + key_name + ' key and ' + security_group_name + ' security group..')

    try:
        new_instance = ec2.create_instances(
            ImageId = 'ami-069116f0fd840fa20',
            MinCount = 1,
            MaxCount = numofinstances,
            InstanceType = 't2.micro',

            ## Security group the instance will abide to (must be in your AWS account);
            SecurityGroups = [security_group_name],

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
    cmd7='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/kindle_reviews.csv'
    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/setup_mysql_new.sh'
    cmd2='chmod +x setup_mysql_new.sh'
    cmd3='sh setup_mysql_new.sh'
    cmd4='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/setup_tables.sh'
    cmd5='chmod +x setup_tables.sh'
    cmd6='sh setup_tables.sh'
    cmds=[cmd7,cmd1,cmd2,cmd3,cmd4,cmd5,cmd6]



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

    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/pipinstalllibs.sh'
    cmd2='chmod +x pipinstalllibs.sh'
    cmd3='sh pipinstalllibs.sh'
    cmd4='git clone https://github.com/yqyqyq123/50.043-project.git'
    text=' '.join(iplist)
    cmd5='echo '+text+'> ip.txt'
    cmd6='echo '+text+'> /home/ubuntu/50.043-project/flaskapp/ip.txt'
    cmd7='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/flask_setup.sh'
    cmd8='screen -d -m bash flask_setup.sh'

    cmds=[cmd1,cmd2,cmd3,cmd4,cmd5,cmd6,cmd7,cmd8]

    try:

        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)
        # Execute a command(cmd) after connecting/ssh to an instance
        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.channel.recv_exit_status() )

        client.close()

    except Exception as e:

        print (e)
#Function for creating a key-pair for EC2 instance
def generate_key_pairs(key_name):  # Key_name needs to be unique *
    outfile = open('{}.pem'.format(key_name),'w')
    key_pair = ec2.create_key_pair(KeyName=key_name)
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)
    # print(KeyPairOut)
    print("Finish creating EC2 key paris")
    os.system("chmod 400 {}.pem".format(key_name))


def main():
    print('This python module will create a AWS EC2 web server instance and execute a web server monitoring script.')
 #####################change security_group_name & key_name
    # security_group_id = 'sg-04db4aa07b4b2d47d'
    security_group_name=input("Please enter the security group name:\n")
    key_name = input("Please enter the key name:\n")
    numofinstances=3

    instance = create_new_webserver_instance(security_group_name, key_name,numofinstances)

    print('Sleeping the program for 60 seconds to let the instance to be configured..')
    time.sleep(90)

    instance[0].reload()
    execute_commands_in_instance_mysql(instance[0].public_ip_address,key_name)
    print('sql setup done')

    instance[1].reload()
    execute_commands_in_instance_mongodb(instance[1].public_ip_address,key_name)
    print('mongodb setup done')

    instance[2].reload()
    print(instance[2].public_ip_address)
    iplist=[]
    iplist=[instance[0].public_ip_address,instance[1].public_ip_address]

    execute_commands_in_instance_server(instance[2].public_ip_address,key_name,iplist)
    print('server setup done, can view in:',instance[2].public_ip_address)


if __name__ == '__main__':
  main()

