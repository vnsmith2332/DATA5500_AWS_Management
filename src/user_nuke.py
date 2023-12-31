import boto3
from constants import STUDENT_IAM_SUBSTRING, STUDENT_GROUP_NAME


def nuke_environments():
    """
    Delete all Cloud9 environments in the account owned by DATA 3500/5500 students.
    Also terminates the EC2 instances on which the environments are running.
    """
    print("Deleting student Cloud9 Environments...")
    
    cloud9_client = boto3.client("cloud9")
    next_token = ""
    
    while True:
        # get all environments, get environment details 25 at a time (defualt)
        list_env_response = cloud9_client.list_environments(nextToken=next_token)
        environment_ids = list_env_response["environmentIds"]
        environment_details = cloud9_client.describe_environments(environmentIds=environment_ids)
        
        # check ownerArn for each env, delete if it belongs to a student
        for env in environment_details["environments"]:
            if STUDENT_IAM_SUBSTRING in env["ownerArn"]:
                cloud9_client.delete_environment(environmentId=env["id"])
                
        # check for more results waiting to be retrieved
        if "nextToken" not in list_env_response.keys():
            break
        next_token = list_env_response["nextToken"]

    print("Successfully deleted environments.\n")


def nuke_users() -> None:
    """
    Delete all IAM users that are student users
    """
    iam_client = boto3.client("iam")

    # delete first batch of student users
    print("Deleting users...")
    list_user_response = iam_client.list_users()
    for user in list_user_response["Users"]:
        if STUDENT_IAM_SUBSTRING in user["UserName"]:
            iam_client.delete_login_profile(UserName=user["UserName"])
            iam_client.remove_user_from_group(GroupName=STUDENT_GROUP_NAME, UserName=user["UserName"])
            iam_client.delete_user(UserName=user["UserName"])

    # delete other batches of student users, if necessary
    while list_user_response["IsTruncated"]:
        list_user_response = iam_client.list_users(Marker=list_user_response["Marker"])
        for user in list_user_response["Users"]:
            if STUDENT_IAM_SUBSTRING in user["UserName"]:
                iam_client.delete_login_profile(UserName=user["UserName"])
                iam_client.remove_user_from_group(GroupName=STUDENT_GROUP_NAME, UserName=user["UserName"])
                iam_client.delete_user(UserName=user["UserName"])
                
    print("Successfully deleted users.\n")
    
if __name__ == "__main__":
    nuke_environments()
    nuke_users()
