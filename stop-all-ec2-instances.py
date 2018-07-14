# Script to stop all running EC2 instances in the default region. Be careful! This will stop all instances
# instantly. Do not use if you have production servers running! Useful to keep EC2 costs down if you want to
# quickly stop your instances without having to specify ids

import boto3
ec2 = boto3.client('ec2')

filters = [{'Name': 'instance-state-name','Values': ['running']}]

# Filter the instances based on filters above
instances = ec2.describe_instances(Filters=filters)

# Instantiate empty array
RunningInstances = []

for res in instances["Reservations"]:
	for instance in res["Instances"]:
		print(instance["InstanceId"] + " is running!")
		RunningInstances.append(instance["InstanceId"])

count_running = len(RunningInstances)

if(count_running > 0):
	choice = input("You are about to stop %d instances, continue? (Y / n): " % (count_running))
	if(choice == 'y' or choice == 'Y'):
		ec2.stop_instances(InstanceIds=RunningInstances, DryRun=False)
		print("Stopping %d instances" % (count_running))
	else:
		print("No instances were stopped")
else:
	print("No instances running")