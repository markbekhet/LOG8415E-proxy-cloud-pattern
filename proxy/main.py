import json
from random_hit import *

f = open("config.json")
data = json.load(f)
private_dns = data["master_dns"]
slave1_ip = data["slave1_ip"]
slave2_ip = data["slave2_ip"]
slave3_ip = data["slave3_ip"]
private_key_file = "key.pem"
 
master_ip = data["master_ip"]

with open_ssh_tunnel(master_ip,slave1_ip,private_key_file) as tunnel:
    mysql_connect(tunnel)
