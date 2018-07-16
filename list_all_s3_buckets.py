#import Boto 3
import boto3

#The AWS service we want to use
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
	print(bucket.name)
input()

