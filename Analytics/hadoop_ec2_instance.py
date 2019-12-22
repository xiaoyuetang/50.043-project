import boto3
import time
import subprocess
import botocore
import paramiko
from botocore.exceptions import ClientError
## Global variable to access EC2 functions provided by Boto3;
ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
# response = ec2.describe_vpcs()
# vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '') #Get VPC id of this aws account
# print(vpc_id)

###########################

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

#    try:
#        response = ec2_client.describe_security_groups(GroupNames=[security_group_name])
#        print("Security group: {} exits".format(security_group_name))
#    #     pp.pprint(response)
#    except ClientError as e:
#    #     pp.pprint(e)
#        print("This security group doesn't exist,creating a new one...\n")
#        create_security_group(security_group_name)


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
            ImageId = 'ami-066fe36434546c9d1',
            MinCount = 1,
            MaxCount = numofinstances,
            InstanceType = 't2.medium',

            ## Security group the instance will abide to (must be in your AWS account);
            SecurityGroups = ['bigdhatta_access'],

            ## Name of private key to be used to launch the instance (should be in the same directory as this file);
            KeyName = key_name,
        )

        print('New instance created (ID: ' + new_instance[0].id + ').')


        return new_instance

    except Exception as error:
        print('An error occured while trying to create a new instance: ' + str(error))

def execute_commands_in_instance_node(public_ip_address,key_name,args):
    print(args)
    key = paramiko.RSAKey.from_private_key_file(key_name+'.pem')

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    instance_ip=public_ip_address
#    cmd1='wget https://kindlemetadata.s3-us-west-2.amazonaws.com/hadoop_setup1.sh'
    cmd1='wget https://bigdhattabucket.s3-ap-southeast-1.amazonaws.com/hadoop_setup3.sh'
    cmd2='chmod +x hadoop_setup3.sh'
    cmd3='./hadoop_setup3.sh ' + args

    try:

        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance

        stdin, stdout, stderr = client.exec_command(cmd1)

        print(stdout.channel.recv_exit_status() )
        stdin, stdout, stderr = client.exec_command(cmd2)

        print(stdout.channel.recv_exit_status() )
        stdin, stdout, stderr = client.exec_command(cmd3,get_pty=True)

        print(stdout.channel.recv_exit_status() )

        # close the client connection once the job is done

        client.close()

    except Exception as e:
        

        print (e)
def main():

    print('This python module will create a AWS EC2 web server instance and execute a web server monitoring script.')
#group3: sql
    security_group_id = 'sg-01af44b05cd683371'
#group1: mongo
    security_group_id1 = 'sg-0509683aa09635a18'
#group4: server
    security_group_id4 = 'sg-04db4aa07b4b2d47d'
    key_name = 'hello'
#group5: had00p
    security_group_id5 = 'sg-011eec6bdbecc0e2b'
    key_name = 'biggerdhatta'


    #create intsance for hadoop
    #namenode
    nodesNum=4
    instances=[]
    ips=[]
    instances=create_new_webserver_instance(security_group_id5, key_name,nodesNum)
    for instance in instances:
        print(instance)
        print('Sleeping the program for 30 seconds to let the instance to be configured..')
        time.sleep(30)
        instance.reload()
        print(instance.public_ip_address)
        ips.append(instance.public_ip_address)        
    print('Picking first created node to be namenode..')
    namenodeip = str(ips[0])
    print(namenodeip)
#	cmd2='chmod +x node_setup.sh'
#    cmdnamenode='sh node_setup.sh'
    nnargstring = ''
    for k in range(len(ips)):
        nnargstring += ips[k] + ' '
    for bleh in range(len(ips)):
        if bleh == 0:
            print('executing command in namenode ' + ips[bleh] + ' with parameters : ' +  nnargstring)
            execute_commands_in_instance_node(ips[bleh],key_name,nnargstring)
        else:
            print('executing command in worker ' + ips[bleh] + '  with parameters : ' + namenodeip)
            execute_commands_in_instance_node(ips[bleh],key_name,namenodeip)

    # execute_commands_in_instance_mysql(public_ip_address,key_name)
    # print('had00p and spahk setup done')



if __name__ == '__main__':
  main()
