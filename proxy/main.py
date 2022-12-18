import json
from random_hit import random_hit
import sys
import paramiko
import pymysql
import random
from customized_hit import customized_hit


def mysql_connect(host_sql, tunnel_port, command):
    """
    A method used by the main function of the proxy pattern implementation
    @param host_sql: The host ip that runs the sql server.
    @param tunnel_port: The port used to connect to the database
    @param command: The command to be executed on the SQL server.
    @return: nothing
    """
    connection = pymysql.connect(
        host=host_sql,
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
    """
    First the method reads the data from the files provided by the local run earlier. After that it starts the proxy
    implementation. The script requires to have at least two arguments to the script.The first being the algorithm to
    be tested and the successive arguments are the SQL commands to be tested against the cluster using the proxy
    pattern. Example of a terminal command will then be: python main.py random_hit "SELECT * FROM actor"
    Read requests are distinguished by the presence of the keyword select at the beginning of the SQL command else
    the command will be considered a write command and it will be redirected to master directly.
    Else if it is a read command, the algorithm entered by the user (first argument) will then be executed to get the
    host, the SQL port to be used and the tunnel created.
    Finally the mysql_connect function will be called using using the information provided as the host and port.
    @return:
    """
    f = open("config.json")
    data = json.load(f)
    ips = []
    ips.append(data["master_ip"])
    ips.append(data["slave1_ip"])
    ips.append(data["slave2_ip"])
    ips.append(data["slave3_ip"])
    private_key_file = "key.pem"
    private_key = paramiko.RSAKey.from_private_key_file(private_key_file)

    if len(sys.argv) < 3:
        print("Please enter an algorithm from direct_hit, random_hit or customized_hit " +
              "followed by an sql command")
        exit(-1)

    commands = sys.argv[2:]
    for command in commands:
        print("executing SQL command {}".format(command))
        tunnel = None
        host = None
        tunnel_port = None

        find_select = command.lower().find("select")

        if find_select == 0:
            print("The command treated is a read command")
            read_algorithm = sys.argv[1]
            if read_algorithm == "random_hit":
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

        if tunnel != None:
            tunnel.stop()


main()
