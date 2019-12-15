cd to Analytics folder to use the following ssh commands

NameNode
ssh -i "ksdbkey.pem" ubuntu@ec2-3-85-48-139.compute-1.amazonaws.com

DataNode1
ssh -i "ksdbkey.pem" ubuntu@ec2-54-209-106-174.compute-1.amazonaws.com
OR
inside NameNode, use: $ssh dnode1

DataNode2
ssh -i "ksdbkey.pem" ubuntu@ec2-3-89-50-211.compute-1.amazonaws.com
OR
inside NameNode, use: $ssh dnode2

DataNode3
ssh -i "ksdbkey.pem" ubuntu@ec2-54-236-235-190.compute-1.amazonaws.com
OR
inside NameNode, use: $ssh dnode3

