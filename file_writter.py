"""
file content:
[ndb_mgmd]
hostname=ip-172-31-95-67.ec2.internal
datadir=/opt/mysqlcluster/deploy/ndb_data
nodeid=1

[ndbd default]
noofreplicas=3

[ndbd]
hostname=ip-172-31-92-164.ec2.internal
nodeid=3
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=ip-172-31-81-136.ec2.internal
nodeid=4
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=ip-172-31-92-207.ec2.internal
nodeid=5
datadir=/opt/mysqlcluster/deploy/ndb_data

[mysqld]
nodeid=50
"""
import os
import json


def write_config_ini_file_content(private_dns_1, private_dns_2, private_dns_3, private_dns_4):
    ret = "[ndb_mgmd] " + "\n" + "hostname={}\n".format(private_dns_1) + \
          "datadir=/opt/mysqlcluster/deploy/ndb_data\n" + "nodeid=1\n" + \
          "[ndbd default]" + "\n" + "noofreplicas=3\n" + \
          "datadir=/opt/mysqlcluster/deploy/ndb_data\n" + "ServerPort=11860\n" +\
          "[ndbd]\nhostname={}\n".format(private_dns_2) \
          + "nodeid=3\n" + \
          "# bind-address={}\n".format(private_dns_2) + \
          "[ndbd]\nhostname={}\n".format(private_dns_3) \
          + "nodeid=4\n" + \
          "# bind-address={}\n".format(private_dns_3) + \
          "[ndbd]\nhostname={}\n".format(private_dns_4) \
          + "nodeid=5\n" + \
          "# bind-address={}\n".format(private_dns_4) + \
          "[mysqld]\nnodeid=50"

    print(ret)
    path_folder = os.path.abspath('cluster')
    path_file = os.path.join(path_folder, 'config.ini')
    f = open(path_file, "w")
    f.write(ret)
    f.close()


def append_to_replica_script(string):
    with open("cluster/slave_mysql_script.sh", "a") as file:
        file.write(string)


def write_config_proxy_file_content(private_dns_master, private_ip_array, private_key):
    ret = { 
        "master_dns": private_dns_master ,
        "master_ip": private_ip_array[0],
        "slave1_ip": private_ip_array[1],
        "slave2_ip": private_ip_array[2] ,
        "slave3_ip": private_ip_array[3]
    }
    path_folder = os.path.abspath('proxy')
    path_file = os.path.join(path_folder, 'config.json')
    f = open(path_file, "w")
    json.dump(ret, f)
    f.close()
    path_file2 = os.path.join(path_folder, 'key.pem')
    f2 = open(path_file2, "w")
    f2.write(private_key)
    f2.close()

def write_sqld_config_file(private_ips):
    ret = "[mysqld]" +\
        "ndbcluster \n" +\
        "datadir=/opt/mysqlcluster/deploy/mysqld_data \n" +\
        "basedir=/opt/mysqlcluster/home/mysqlc \n" +\
        "port=3306 \n" +\
        "bind-address=0.0.0.0"
    #for ip in private_ips:
    #    ret += "bind-address={0}\n".format(ip)

    path_folder = os.path.abspath('cluster')
    path_file = os.path.join(path_folder, 'my.cnf')
    f = open(path_file, "w")
    f.write(ret)
    f.close()

if __name__ == "__main__":
    write_config_ini_file_content("lb-619373195.us-east-1.elb.amazonaws.com")
