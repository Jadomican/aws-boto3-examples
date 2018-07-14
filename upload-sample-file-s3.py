#Uploads a sample file to a specified S3 bucket

#import Boto 3
import boto3

#import os to create a sample file
import os

#The AWS service we want to use
s3 = boto3.resource('s3')

#Take the name of the bucket as a user input
bucket_name = input('Enter your bucket name: ')
my_bucket = s3.Bucket(bucket_name)
file_name = 'sample-boto-upload.txt'

#Create a sample file in the current directory
file = open(os.path.join(os.getcwd(), file_name), 'w')
file.write('This is a sample Boto 3 S3 upload!')
file.close()

#Upload the sample data
data = open(file_name, 'rb')
my_bucket.put_object(Key=file_name, Body=data)
print("\nUploaded %s!" % (file_name))

#View the bucket contents
print("\n\n--- Conents of %s ---\n" % (bucket_name))
for object in my_bucket.objects.all():
    print(object)

data.close()
