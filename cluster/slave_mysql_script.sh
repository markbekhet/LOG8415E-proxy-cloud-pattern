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