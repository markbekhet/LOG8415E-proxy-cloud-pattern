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


def write_file_content(private_dns_1, private_dns_2, private_dns_3, private_dns_4):
    ret = "[ndb_mgmd] " + "\n" + "hostname={}\n".format(private_dns_1) +\
          "datadir=/opt/mysqlcluster/deploy/ndb_data\n" + "nodeid=1\n" +\
          "[ndbd default]" + "\n" + "noofreplicas=3\n" + \
          "[ndbd]\nhostname={}\n".format(private_dns_2)\
          + "nodeid=3\ndatadir=/opt/mysqlcluster/deploy/ndb_data\n" + \
          "[ndbd]\nhostname={}\n".format(private_dns_3) \
          + "nodeid=4\ndatadir=/opt/mysqlcluster/deploy/ndb_data\n" + \
            "[ndbd]\nhostname={}\n".format(private_dns_4)\
          + "nodeid=5\ndatadir=/opt/mysqlcluster/deploy/ndb_data\n" + \
            "[mysqld]\nnodeid=50"

    print(ret)
    path_folder = os.path.abspath('cluster')
    path_file = os.path.join(path_folder, 'config.ini')
    f = open(path_file, "w")
    f.write(ret)
    f.close()

def append_to_replica_script(string):
  with open("cluster/slave_mysql_script.sh","a") as file:
    file.write(string)

if __name__ == "__main__":
    write_file_content("lb-619373195.us-east-1.elb.amazonaws.com")
