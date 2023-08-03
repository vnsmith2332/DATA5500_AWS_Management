import boto3
cloud9_client = boto3.client("cloud9")
for id in cloud9_client.list_environments()["environmentIds"]:
    print(cloud9_client.describe_environments(environmentIds=[id]))
    input()
