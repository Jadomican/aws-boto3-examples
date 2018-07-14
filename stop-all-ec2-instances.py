# Script to stop all running EC2 instances by region. Be careful! This will stop all instances instantly. Do not
# use if you have production servers running! Useful to keep EC2 costs down if you want to quickly stop your 
# instances without having to specify ids/ regions. You will be prompted to stop instances per region. (Y / n)

import boto3

def stop_function(region):
	ec2 = boto3.client('ec2', region_name=region)
	print("Checking %s..." % (region))

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

# Fetch all current AWS regions (expect more over time)
client = boto3.client('ec2')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

for region_names in regions:
	stop_function(region_names)
