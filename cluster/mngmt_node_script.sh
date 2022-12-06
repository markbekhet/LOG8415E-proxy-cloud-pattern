sudo apt-get update && sudo apt-get install libncurses5 -y
sudo mkdir -p /opt/mysqlcluster/home
cd /opt/mysqlcluster/home
sudo wget http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
sudo tar -xvf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz

sudo ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc

echo export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc | sudo tee /etc/profile.d/mysqlc.sh

echo export PATH=$MYSQLC_HOME/bin:$PATH | sudo tee -a /etc/profile.d/mysqlc.sh

source /etc/profile.d/mysqlc.sh

sudo mkdir -p /opt/mysqlcluster/deploy

cd /opt/mysqlcluster/deploy

sudo mkdir conf

sudo mkdir mysqld_data
sudo mkdir ndb_data
cd conf

echo "
[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/opt/mysqlcluster/home/mysqlc
port=3306" | sudo tee my.cnf

#string to be written automatically by the python script

sudo cp ~/config.ini config.ini

cd /opt/mysqlcluster/home/mysqlc
sudo scripts/mysql_install_db --no-defaults --datadir=/opt/mysqlcluster/deploy/mysqld_data

sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial --configdir=/opt/mysqlcluster/deploy/conf/