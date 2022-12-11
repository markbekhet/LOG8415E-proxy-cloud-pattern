import subprocess
import re
from random_hit import open_ssh_tunnel
import sys

def ping_server(server_ip):
    output = subprocess.check_output(['ping', '-c', '3', server_ip])
    output = output.decode('utf8')
    statistic = re.search(r'(\d+\.\d+/){3}\d+\.\d+', output).group(0)
    avg_time = re.findall(r'\d+\.\d+', statistic)[1]
    response_time = float(avg_time)
    return response_time

def customized_hit(private_ips, key):
    min_time = sys.float_info.max
    chosen_data_node = 0
    for i in range(1,4):
        ping_time = ping_server(private_ips[i])
        if  ping_time < min_time:
            min_time = ping_time
            chosen_data_node  = i
    
    print("The chosen data node based on response time is {}".format(chosen_data_node))
    return open_ssh_tunnel(private_ips[0], private_ips[chosen_data_node], key)