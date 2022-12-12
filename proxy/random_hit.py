from sshtunnel import SSHTunnelForwarder
import random


def open_ssh_tunnel(master_ip, slave_ip,rsa_key):
    tunnel = SSHTunnelForwarder(
        (slave_ip, 22),
        ssh_username = "ubuntu",
        ssh_pkey=rsa_key,
        remote_bind_address = (master_ip,3306)
    )
    tunnel.start()
    return tunnel


def random_hit(private_ips,key):
    rand = random.randint(1,3)
    print("The random function chose to contact the datanode {}".format(rand))
    return open_ssh_tunnel(private_ips[0], private_ips[rand], key)