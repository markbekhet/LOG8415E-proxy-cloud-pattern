import json
from random_hit import random_hit
import sys
import paramiko
import pymysql
import random
from customized_hit import customized_hit


"""
    @param tunnel: The tunnel created by the functions 
            random_hit, direct_hit or customized_hit
    @param commands: SQL commands to be executed

    This function will be used by the main function to test the well behaviour
    of the proxy

    The idea is that we must be able to connect to the database through the proxy.
    Hence, the host should always be the public ip of the proxy server. 
"""
def mysql_connect(host_sql,tunnel_port, command):
    connection = pymysql.connect(
        host = host_sql,
        user="sbtest",
        password="passw0rd",
        db="sakila",
        port=tunnel_port,
        autocommit=True
    )
    cursor = connection.cursor()
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
        print("Please enter an sql command")
        exit(-1)

    commands = sys.argv[1:]
    for command in commands:
        print("executing SQL command {}".format(command))
        tunnel = None
        host = None
        tunnel_port = None

        find_select = command.lower().find("select")

        if find_select == 0:
            print("The command treated is a read command")
            read_algorithm = random.randint(0,1)
            if read_algorithm == 0:
                print("The algorithm chosen for this request is random hit.")
                tunnel = random_hit(ips, private_key)
                tunnel_port = tunnel.local_bind_port
                host = '127.0.0.1'
            else:
                ##TODO: Add the option for the cutomized hit
                print("The algorithm chosen for this request is customized hit.")
                tunnel = customized_hit(ips, private_key)
                tunnel_port = tunnel.local_bind_port
                host = '127.0.0.1'
        else:
            print("The command treated is a write command. Therefore, using the direct hit algorithm.")
            host = ips[0]
            tunnel_port = 3306
        
        
        mysql_connect(host, tunnel_port, command)
        
        if tunnel!= None:
            tunnel.stop()


main()