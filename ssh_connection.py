import paramiko
import scp
from scp import SCPClient
from io import StringIO
import os


def start_deployment(ip, files, commands, key_material):
    """
    This function starts the deployment process for the instance with the provided ip address.
    The deployment script is running on the instance. The provided deployment commands are also
    running on the instance before closing the connection.
    """
    connection = None
    ftp_client = None
    try:
        connection = instance_connection(ip, key_material)
        transfer_file(connection, files)
        run_commands(connection, commands)
        ftp_client = connection.open_sftp()
        ftp_client.get("/home/ubuntu/time_results.txt", os.path.join(os.path.curdir, "time_results.txt"))
        ftp_client.get("/home/ubuntu/benchmarking_time_results.txt", os.path.join(os.path.curdir, "benchmarking_time_results.txt"))
        ftp_client.get("/home/ubuntu/friends_suggestion_solution.txt", os.path.join(os.path.curdir, "friends_suggestion_solution.txt"))
        ftp_client.get("/home/ubuntu/Average_benchmark_hadoop_spark.png",
                       os.path.join(os.path.curdir, "Average_benchmark_hadoop_spark.png"))
        ftp_client.get("/home/ubuntu/Average_benchmark_hadoop_linux.png",
                       os.path.join(os.path.curdir, "Average_benchmark_hadoop_linux.png"))
    except Exception as e:
        print(e)
    finally:
        if ftp_client is not None:
            ftp_client.close()

        if connection is not None:
            connection.close()


def instance_connection(instance_ip, key_material):
    """
    This function initialize a connection with the ec2 instance.
    """
    ssh_username = "ubuntu"
    ssh_key_file = StringIO(key_material)
    rsa_key = paramiko.RSAKey.from_private_key(ssh_key_file)
    # rsa_key = paramiko.RSAKey.from_private_key_file("labsuser.pem")
    ssh_connection = paramiko.SSHClient()
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connection.connect(hostname=instance_ip, username=ssh_username,
                           pkey=rsa_key, allow_agent=False, look_for_keys=False)
    print("connection success")
    return ssh_connection


def transfer_file(ssh_connection, files):
    """
    Initializes a SCP connection using a SSH connection and tranfert the file to the instance connected 
    to the session.
    """
    scp_connection = SCPClient(ssh_connection.get_transport())
    for file in files:
        scp_connection.put(file, remote_path='/home/ubuntu')


def run_commands(ssh_connection, commands):
    """
    Executes a list of bash commands in the instance connected to the SSH session.
    """
    for command in commands:
        print("running command: {}".format(command))
        _, stdout, stderr = ssh_connection.exec_command(command)
        print(stdout.read())
        print(stderr.read())


if __name__ == "__main__":
    connection = instance_connection("18.232.164.184")
    run_commands(connection, ["mkdir folder", "cd folder", "ls"])
    connection.close()
