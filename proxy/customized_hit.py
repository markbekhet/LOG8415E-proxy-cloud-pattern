import subprocess
import re
from random_hit import open_ssh_tunnel
import sys


def ping_server(server_ip):
    """
    This function pings the server identified by the ip passed as a parameter 3 times and returns the average
    time taken by the ping
    @param server_ip: The server to be pinged
    @return: The average response return time
    """
    output = subprocess.check_output(['ping', '-c', '3', server_ip])
    output = output.decode('utf8')
    statistic = re.search(r'(\d+\.\d+/){3}\d+\.\d+', output).group(0)
    avg_time = re.findall(r'\d+\.\d+', statistic)[1]
    response_time = float(avg_time)
    return response_time


def customized_hit(private_ips, key):
    """
    For every ip in the list of private_ips designing a datanode provided in the parameters, ping the server
    Compare the ping time and take the server with the least average returned by the ping operation
    Then use the method open_ssh_tunnel provided by the random_hit.py file to open an ssh tunnel.
    @param private_ips: The list of private_ips of the servers of the cluster
    @param key: The key used to ssh tunnel to the server used by open_ssh_tunnel method
    @return: The tunnel created by the method open_ssh_tunnel
    """
    min_time = sys.float_info.max
    chosen_data_node = 0
    for i in range(1, 3):
        ping_time = ping_server(private_ips[i])
        if ping_time < min_time:
            min_time = ping_time
            chosen_data_node = i

    print("The chosen data node based on response time is {}".format(chosen_data_node))
    return open_ssh_tunnel(private_ips[0], private_ips[chosen_data_node], key)
