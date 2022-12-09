import pymysql
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import paramiko
from io import StringIO


def open_ssh_tunnel(master_ip, slave_ip,ssh_key_file):
    rsa_key = paramiko.RSAKey.from_private_key_file(ssh_key_file)
    tunnel = SSHTunnelForwarder(
        (slave_ip, 22),
        ssh_username = "ubuntu",
        ssh_pkey=rsa_key,
        remote_bind_address = (master_ip,3306)
    )
    tunnel.start()
    return tunnel

def mysql_connect(tunnel):
    connection = pymysql.connect(
        host = '127.0.0.1',
        user="sbtest",
        password="passw0rd",
        db="sakila",
        port=tunnel.local_bind_port
    )
    cursor = connection.cursor()
    cursor.execute("select * from actor")
    output = cursor.fetchall()
    print(output)
