from sshtunnel import SSHTunnelForwarder
import random


def open_ssh_tunnel(master_ip, slave_ip,rsa_key):
    """
    The method ssh into the server from which it will remotely bind to the master node mysqld server
    to fetch the mysql api. This way we can guarantee that the data node is the one responding with its own data
    because it has only requested the API from the master ip. That's due because the datanode doesn't run a mysqld
    server. After creating the tunnel. The tunnel is started and then returned to be latter used by the main function
    @param master_ip: the ip of the master node
    @param slave_ip: The ip of the datanode to which we want to ssh
    @param rsa_key: The key used to successfully ssh into the datanode
    @return: The tunnel created by the method
    """
    tunnel = SSHTunnelForwarder(
        (slave_ip, 22),
        ssh_username = "ubuntu",
        ssh_pkey=rsa_key,
        remote_bind_address = (master_ip,3306)
    )
    tunnel.start()
    return tunnel


def random_hit(private_ips,key):
    """
    This method randomly chooses a number between 1 and 3 inclusively, those are the indexes of the datanode ips
    as provided by the main function and then it open an ssh tunnel with the server randomly chosen.
    @param private_ips: The ips of the nodes of the cluster
    @param key: The key used to connect ssh with the datanode
    @return: The tunnel created.
    """
    rand = random.randint(1,3)
    print("The random function chose to contact the datanode {}".format(rand))
    return open_ssh_tunnel(private_ips[0], private_ips[rand], key)