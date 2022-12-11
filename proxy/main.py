import json
from random_hit import random_hit
import sys
from direct_hit import direct_hit
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
def mysql_connect(tunnel, commands):
    connection = pymysql.connect(
        host = '127.0.0.1',
        user="sbtest",
        password="passw0rd",
        db="sakila",
        port=tunnel.local_bind_port,
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
    
    algorithm = sys.argv[1]
    tunnel = None;
    match algorithm:
        case "direct_hit":
            tunnel = direct_hit(ips[0], private_key)
        case "random_hit":
            tunnel = random_hit(ips, private_key)
        case _:
            print("supported algorithms are direct_hit and random_hit")
            exit(-1)
    
    mysql_connect(tunnel, ["SELECT * FROM actor"])
    tunnel.stop()


main()