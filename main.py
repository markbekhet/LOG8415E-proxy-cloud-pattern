import boto3
from instances import *
import os
from ssh_connection import *
from security_group import *
from file_writter import *

def prepare_cluster_and_test_proxy(ec2_resource, ec2_client, instance_ami, key_pair, security_group_id):
    cluster_instances_tag = "cluster_instances"
    cluster_instances=None
    proxy_instance = None
    try:
        sn_all = ec2_client.describe_subnets()
        subnet = None
        for sn in sn_all['Subnets']:
            if sn['AvailabilityZone'] == 'us-east-1a' or sn['AvailabilityZone'] == 'us-east-1b':
                subnet = sn['SubnetId']
        proxy_tag = "proxy_server"
        create_instances(ec2_resource, instance_ami, "t2.micro",
                                    key_pair["KeyName"], cluster_instances_tag,
                                     4, security_group_id, subnet)[0]
        create_instances(ec2_resource, instance_ami, "t2.large",
                                    key_pair["KeyName"], proxy_tag,
                                     1, security_group_id, subnet)[0]
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
        private_ips = [instance.private_ip_address for instance in cluster_instances.all()]

        print(public_ips)
        write_config_ini_file_content(private_dns_1=private_dns[0],
            private_dns_2=private_ips[1],
            private_dns_3=private_ips[2],
            private_dns_4=private_ips[3])

        write_config_proxy_file_content(private_dns_master=private_dns[0],
            private_ip_array=private_ips, private_key=key_pair["KeyMaterial"])

        #write_sqld_config_file(private_ips)

        mngmt_node_coomands = [
            "sudo apt-get update && sudo apt-get install git -y",
            "chmod 777 mngmt_node_script.sh",
            "./mngmt_node_script.sh",
            "sudo apt install screen -y",
            "/usr/bin/screen -dm sudo /opt/mysqlcluster/home/mysqlc/bin/mysqld --defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf --user=root"
        ]

        benchmarking_commands = [
            "sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show",
            "wget https://downloads.mysql.com/docs/sakila-db.tar.gz",
            "tar -xf sakila-db.tar.gz",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"SOURCE sakila-db/sakila-data.sql\"",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"create database dbtest\"",
            "sudo apt-get install sysbench -y",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"SOURCE sakila-db/sakila-schema.sql\"",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"SOURCE sakila-db/sakila-data.sql\"",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"CREATE USER \'sbtest\'@\'%\' IDENTIFIED BY \'passw0rd\'\"",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"GRANT ALL PRIVILEGES ON sakila.* TO \'sbtest\'@\'%\'\"",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"FLUSH PRIVILEGES\"",
            "sudo /opt/mysqlcluster/home/mysqlc/bin/mysql -e \"GRANT ALL PRIVILEGES ON dbtest.* TO \'sbtest\'@\'%\'\"",
            "sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila --mysql-host={0} --mysql-user=sbtest --mysql-password=passw0rd --table_size=10000 prepare".format(private_dns[0]),
            "sudo sysbench --test=oltp_read_write --threads=6 --max-time=300 --tables=23 --mysql-db=sakila --mysql-host={0} --mysql-user=sbtest --mysql-password=passw0rd --table_size=10000 run > benchmark_cluster.txt".format(private_dns[0]),
            "sudo sysbench --test=oltp_read_write --tables=23 --mysql-db=sakila --mysql-host={0} --mysql-user=sbtest --mysql-password=passw0rd --table_size=10000 cleanup".format(private_dns[0])

        ]

        proxy_commands = [
            "chmod 777 proxy/setup_proxy.sh",
            "chmod 777 proxy/test_setup.sh",
            "./proxy/setup_proxy.sh",
            "./proxy/test_setup.sh"
        ]
        time.sleep(60)
        cluster_folder = os.path.abspath('cluster')
        #The mngmt node

        mngmt_node_files = [
            os.path.join(cluster_folder, "config.ini"),
            os.path.join(cluster_folder, "mngmt_node_script.sh"),
        ]
        start_deployment(public_ips[0], mngmt_node_coomands,key_pair["KeyMaterial"], 
                    mngmt_node_files)

        print("Done mgmt node deployment")
        time.sleep(60)
        replica_file = [
            os.path.join(cluster_folder, "slave_mysql_script.sh")
        ]

        #The replicas
        replicas_threads = []

        for i in range(1, 4):
            replicas_commands = [
                "chmod 777 slave_mysql_script.sh",
                "./slave_mysql_script.sh",
                "sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c \"{0}:1186;bind-address={1}\"".
                    format(private_dns[0], private_ips[i])
            ]
            ip = public_ips[i]
            print("Deploying replica node {0}".format(ip))
            thread = Thread(target=start_deployment, args=(ip, replicas_commands, key_pair["KeyMaterial"] ,replica_file))
            thread.start()
            replicas_threads.append(thread)
    
        for thread in replicas_threads:
            thread.join()

        print("Done replica nodes deployment")
        
        start_deployment(public_ips[0], benchmarking_commands, key_pair["KeyMaterial"], 
            fetch_file="benchmark_cluster.txt", is_recursive=False)
    
        proxy_instances_list = ec2_resource.instances.filter(
                Filters=[
                    {'Name': 'instance-state-name', 'Values': ['running']},
                    {'Name': 'tag:Name', 'Values': [proxy_tag]}
                ]
            )
        for instance in proxy_instances_list.all():
            print("Found proxy")
            proxy_instance = instance
        
        proxy_folder = [os.path.abspath("proxy")]
        print(proxy_instance.public_ip_address)
        start_deployment(proxy_instance.public_ip_address, proxy_commands,key_pair["KeyMaterial"], 
                    proxy_folder,fetch_file="test_proxy.txt",is_recursive=True)
    except Exception as e:
        print(e)
    finally:
        if proxy_instance is not None:
            proxy_instance.terminate()
            proxy_instance.wait_until_terminated()

        if cluster_instances is not None:
            for instance in cluster_instances.all():
                instance.terminate()

            for instance in cluster_instances.all():
                instance.wait_until_terminated()

def test_standalone_mysql(ec2_resource, ec2_client, instance_ami, key_pair, security_group_id):
    standalone_tag = "standalone"
    standalone_instances = None
    try:
        sn_all = ec2_client.describe_subnets()
        subnet = None
        for sn in sn_all['Subnets']:
            if sn['AvailabilityZone'] == 'us-east-1a' or sn['AvailabilityZone'] == 'us-east-1b':
                subnet = sn['SubnetId']
        create_instances(ec2_resource, instance_ami, "t2.micro",
                                    key_pair["KeyName"], standalone_tag,
                                     1, security_group_id, subnet)[0]
        awake = False
        while awake is False:
            standalone_instances = ec2_resource.instances.filter(
                Filters=[
                    {'Name': 'instance-state-name', 'Values': ['running']},
                    {'Name': 'tag:Name', 'Values': [standalone_tag]}
                ]
            )
            if len(list(standalone_instances.all())) == 1:
                awake = True
            else:
                time.sleep(0.5)

        public_ips = [instance.public_ip_address for instance in standalone_instances.all()]
        
        print(public_ips)

        standalone_commands = [
            "chmod 777 standalone_mysql_script.sh",
            "./standalone_mysql_script.sh",
        ]

        time.sleep(60)
        current_folder = os.path.curdir
        #The mngmt node

        standalone_files = [
            os.path.join(current_folder, "standalone_mysql_script.sh")
        ]

        start_deployment(public_ips[0], standalone_commands,key_pair["KeyMaterial"], 
                    standalone_files,fetch_file="benchmark_standalone.txt")

    except Exception as e:
        print(e)
    finally:
        if standalone_instances is not None:
            for instance in standalone_instances.all():
                instance.terminate()

            for instance in standalone_instances.all():
                instance.wait_until_terminated()
        

def main():
    session = boto3.Session(profile_name='default')
    ec2_client = session.client('ec2')
    ec2_resource = session.resource('ec2')

    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')

    instance_ami = 'ami-08c40ec9ead489470'
    key_pair = create_key_pair(ec2_client, "tp3Key")
    security_group_id = create_security_group(ec2_client, vpc_id)['GroupId']
    test_standalone_mysql(ec2_resource, ec2_client, instance_ami, key_pair, security_group_id)
    prepare_cluster_and_test_proxy(ec2_resource, ec2_client, instance_ami, key_pair, security_group_id)

    
    ec2_client.delete_key_pair(KeyName="tp3Key")
    time.sleep(60)
    try:
        delete_security_group(ec2_client, security_group_id)
    except:
        time.sleep(30)
        delete_security_group(ec2_client, security_group_id)

main()