import boto3
from instances import *
import os
from ssh_connection import *
from security_group import *
from file_writter import *

session = boto3.Session(profile_name='default')
ec2_client = session.client('ec2')
ec2_resource = session.resource('ec2')

vpcs = ec2_client.describe_vpcs()
vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')

instance_ami = 'ami-08c40ec9ead489470'
key_pair = create_key_pair(ec2_client, "tp3Key")
security_group_id = create_security_group(ec2_client, vpc_id)['GroupId']

cluster_instances_tag = "cluster_instances"
cluster_instances=None
try:
    create_instances(ec2_resource, instance_ami, "t2.micro",
                                key_pair["KeyName"], cluster_instances_tag, 4, security_group_id)[0]

    awake = False
    while awake is False:
        cluster_instances = ec2_resource.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': [cluster_instances_tag]}
            ]
        )
        if len(list(cluster_instances.all())) == 4:
            awake = True
        else:
            time.sleep(0.5)
        
    private_dns = [instance.private_dns_name for instance in cluster_instances.all()]
    public_ips = [instance.public_ip_address for instance in cluster_instances.all()]
    print(public_ips)
    write_file_content(private_dns_1=private_dns[0],
        private_dns_2=private_dns[1],
        private_dns_3=private_dns[2],
        private_dns_4=private_dns[3])

    mngmt_node_coomands = [
        "sudo apt-get update && sudo apt-get install git -y",
        "chmod 777 mngmt_node_script.sh",
        "./mngmt_node_script.sh"
    ]

    replicas_commands = [
        "chmod 777 slave_mysql_script.sh",
        "./slave_mysql_script.sh"
    ]

    main_node_commands = [
        "chmod 777 master_mysql_script.sh",
        "./master_mysql_script.sh",
        "/usr/bin/screen -dm sudo /opt/mysqlcluster/home/mysqlc/bin/mysqld --defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf --user=root",
        "sleep 60",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show",
        "wget https://downloads.mysql.com/docs/sakila-db.tar.gz",
        "tar -xf sakila-db.tar.gz",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"SOURCE sakila-db/sakila-data.sql\"",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"create database dbtest\"",
        "sudo apt-get install sysbench -y",
        "ps aux | grep mysql",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"SOURCE sakila-db/sakila-schema.sql\"",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"CREATE USER \'sbtest\'@\'%\' IDENTIFIED BY \'passw0rd\'\"",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"GRANT ALL PRIVILEGES ON sakila.* TO \'sbtest\'@\'%\'\"",
        "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"GRANT ALL PRIVILEGES ON dbtest.* TO \'sbtest\'@\'%\'\"",
        "sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila --mysql-host={0} --mysql-user=sbtest --mysql-password=passw0rd --table_size=1000 prepare".format(private_dns[0]),
        "sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila --mysql-host={0} --mysql-user=sbtest --mysql-password=passw0rd --table_size=1000 run > benchmark_cluster.txt".format(private_dns[0]),
        "sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila --mysql-host={0} --mysql-user=sbtest --mysql-password=passw0rd --table_size=1000 cleanup".format(private_dns[0])

    ]
    
    connect_to_mngmt= "sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c {0}:1186".format(private_dns[0])
    append_to_replica_script(connect_to_mngmt)

    time.sleep(60)
    cluster_folder = os.path.abspath('cluster')
    #The mngmt node
    mngmt_node_files = [
        os.path.join(cluster_folder, "config.ini"),
        os.path.join(cluster_folder, "mngmt_node_script.sh"),
    ]
    start_deployment(public_ips[0], mngmt_node_coomands,mngmt_node_files, key_pair["KeyMaterial"], False)
    print("Done mgmt node deployment")
    
    replica_file = [
        os.path.join(cluster_folder, "slave_mysql_script.sh")
    ]

    main_node_file = [
        os.path.join(cluster_folder, "master_mysql_script.sh")
    ]
    #The replicas
    replicas_threads = []
    
    for i in range(1,4):
        ip = public_ips[i]
        print("Deploying replica node {0}".format(ip))
        thread = Thread(target=start_deployment, args=(ip, replicas_commands,replica_file, key_pair["KeyMaterial"], False))
        thread.start()
        replicas_threads.append(thread)
    
    for thread in replicas_threads:
        thread.join()
    
    print("Done replica nodes deployment")

    start_deployment(public_ips[0], main_node_commands, main_node_file, key_pair["KeyMaterial"], True)

except Exception as e:
    print(e)
finally:
    if cluster_instances is not None:
        for instance in cluster_instances.all():
            instance.terminate()
        
        for instance in cluster_instances.all():
            instance.wait_until_terminated()

    ec2_client.delete_key_pair(KeyName="tp3Key")
    delete_security_group(ec2_client, security_group_id)

