import boto3
import json

ec2 = boto3.client('ec2')

filters = [{'Name': 'instance-state-name','Values': ['running']}]

#Filter the instances based on filters above
instances = ec2.describe_instances(Filters=filters)
#instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name','Values': ['running']}])

#Instantiate empty array
RunningInstances = []
print("\n")
for res in instances["Reservations"]:
	for instance in res["Instances"]:
		print(instance["InstanceId"] + " stopping!")
		RunningInstances.append(instance["InstanceId"])
		ec2.stop_instances(InstanceIds=RunningInstances, DryRun=False)
