# Script to stop all running EC2 instances by region. Be careful! This will stop all instances instantly. Do not
# use if you have production servers running! Useful to keep EC2 costs down if you want to quickly stop your 
# instances without having to specify ids/ regions. You will be prompted to stop instances per region. (Y / n)
# You can pass command line arguments including -y or -Y to bypass instance stop prompt

import boto3
import sys

#The various YES flags this program can accept
yes_list = ['y', 'Y', '-y', '-Y', 'yes', 'YES']

# Check for running instances in each region. Prompt user before stopping (unless YES flag provided)
def check_instance_states(region):
        ec2 = boto3.client('ec2', region_name=region)
        print("\nChecking %s..." % (region))

        filters = [{'Name': 'instance-state-name','Values': ['running']}]

        # Filter the instances based on filters above
        instances = ec2.describe_instances(Filters=filters)

        # Instantiate empty array
        RunningInstances = []

        for res in instances["Reservations"]:
                for instance in res["Instances"]:
                        print('{} in {} ({}) is running!'.format(instance["InstanceId"], instance["SubnetId"], instance["VpcId"]))
                        RunningInstances.append(instance["InstanceId"])

        count_running = len(RunningInstances)

        if(count_running > 0):
                if(flag not in yes_list):
                        choice = input("You are about to stop %d instances, continue? (Y / n): " % (count_running))
                        if(choice in yes_list):
                                stop_instances(ec2, RunningInstances, count_running)
                        else:
                                print("No instances were stopped")
                else:
                        stop_instances(ec2, RunningInstances, count_running)
        else:
                print("No instances running")

# Perform actual instance stop using the EC2 client                
def stop_instances(ec2_client, running_instances, count_stopping):
        ec2_client.stop_instances(InstanceIds=running_instances, DryRun=False)
        print("Stopping %d instances" % (count_stopping))

# Fetch all current AWS regions (expect more over time)
client = boto3.client('ec2')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

# Check for command line arguments (-y, -Y, y, Y)
if(len(sys.argv) > 1):
        flag = sys.argv[1]
else:
        flag = '-1'

for region_names in regions:
        check_instance_states(region_names)
