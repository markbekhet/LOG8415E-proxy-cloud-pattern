import json
from random_hit import random_hit
import sys
import paramiko
import pymysql


"""
    @param tunnel: The tunnel created by the functions 
            random_hit, direct_hit or customized_hit
    @param commands: SQL commands to be executed

    This function will be used by the main function to test the well behaviour
    of the proxy

    The idea is that we must be able to connect to the database through the proxy.
    Hence, the host should always be the public ip of the proxy server. 
"""
def mysql_connect(host_sql,tunnel_port, commands):
    connection = pymysql.connect(
        host = host_sql,
        user="sbtest",
        password="passw0rd",
        db="sakila",
        port=tunnel_port,
        autocommit=True
    )
    cursor = connection.cursor()
    for command in commands:
        cursor.execute(command)
        output = cursor.fetchall()
        print(output)
    
    connection.close()


def main():
    f = open("config.json")
    data = json.load(f)
    ips = []
    ips.append(data["master_ip"])
    ips.append(data["slave1_ip"])
    ips.append(data["slave2_ip"])
    ips.append(data["slave3_ip"])
    private_key_file = "key.pem"
    private_key = paramiko.RSAKey.from_private_key_file(private_key_file)
    
    if len(sys.argv) < 2:
        print("The algorithm name must be provided as an argument")
        exit(-1)

    algorithm = sys.argv[1]
    tunnel = None
    host = None
    tunnel_port = None
    match algorithm:
        case "direct_hit":
            host = ips[0]
            tunnel_port = 3306
        case "random_hit":
            tunnel = random_hit(ips, private_key)
            tunnel_port = tunnel.local_bind_port
            host = '127.0.0.1'
        case _:
            print("supported algorithms are direct_hit and random_hit")
            exit(-1)
    
    mysql_connect(host, tunnel_port, ["SELECT * FROM actor"])
    
    if tunnel!= None:
        tunnel.stop()


main()