import boto3
from instances import *
import os
from ssh_connection import *
from security_group import *

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
    print(private_dns)
    
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

