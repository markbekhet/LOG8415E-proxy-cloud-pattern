from sshtunnel import SSHTunnelForwarder

def direct_hit(master_ip, rsa_key):
    tunnel = SSHTunnelForwarder(
        (master_ip, 22),
        ssh_username = "ubuntu",
        ssh_pkey=rsa_key,
        remote_bind_address = (master_ip,3306)
    )
    tunnel.start()
    return tunnel
