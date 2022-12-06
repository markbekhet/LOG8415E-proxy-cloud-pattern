sudo apt-get update && sudo apt-get install libncurses5 -y
sudo mkdir -p /opt/mysqlcluster/home
cd /opt/mysqlcluster/home
sudo wget http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
sudo tar -xvf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz

sudo ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc

echo export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc | sudo tee /etc/profile.d/mysqlc.sh

echo export PATH=$MYSQLC_HOME/bin:$PATH | sudo tee -a /etc/profile.d/mysqlc.sh

source /etc/profile.d/mysqlc.sh

sudo mkdir -p /opt/mysqlcluster/deploy/ndb_data

# The hostname of the mngmt node will be used before the port
sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-83-113.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-31-39.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-26-219.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-93-140.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-29-90.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-94-43.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-82-79.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-85-48.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-19-185.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-88-214.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-84-149.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-16-82.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-17-190.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-85-191.ec2.internal:1186sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c ip-172-31-94-87.ec2.internal:1186