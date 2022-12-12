sudo apt update
sudo apt install mysql-server -y

wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz
sudo mysql -e "SOURCE sakila-db/sakila-schema.sql"
sudo mysql -e "SOURCE sakila-db/sakila-data.sql"
sudo apt-get install sysbench -y
sudo mysql -e "CREATE USER 'sbtest'@'%' IDENTIFIED BY 'passw0rd'"
sudo mysql -e "GRANT ALL PRIVILEGES ON sakila.* TO 'sbtest'@'%'"

sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila \
 --mysql-user=sbtest --mysql-password=passw0rd --table_size=10000 prepare

sudo sysbench --test=oltp_read_write --threads=6 --max-time=300 --tables=23 --mysql-db=sakila \
 --mysql-user=sbtest --mysql-password=passw0rd --table_size=10000 run > benchmark_standalone.txt

sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila \
 --mysql-user=sbtest --mysql-password=passw0rd --table_size=10000 cleanup

