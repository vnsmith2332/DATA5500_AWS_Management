import boto3
import string
from constants import STUDENT_GROUP_NAME, STUDENT_IAM_SUBSTRING, SENDER_EMAIL, AWS_ROOT_ACCT_ID, COURSES, PASSWORD


class User():
    def __init__(self, first_name: str, last_name: str, a_number: str, email: str, section: str):
        self.__first_name = first_name.lower()
        self.__last_name = last_name.lower()
        self.__a_number = a_number.lower()
        self.__email = email.lower()
        self.__username = self.__first_name + "." + self.__last_name + STUDENT_IAM_SUBSTRING
        self.__password = PASSWORD
        
        for course in COURSES.keys():
            if course in section:
                self.__course = COURSES[course]
                break
          
    
    
    def get_arn(self):
        return self.__user_arn
        
        
    def get_first_name(self):
        return self.__first_name
        
        
    def get_last_name(self):
       return self.__last_name
        
        
    def get_a_number(self):
        return self.__last_name
    
    
    def get_email(self):
        return self.__email
        
        
    def get_username(self):
        return self.__username
        
    
    def get_password(self):
        return self.__password
        
        
    def get_course(self):
        return self.__course
        
        
    def create_user(self):
        iam_client = boto3.client("iam")
        
        # creating the user
        tags = [
            {
                "Key": "a_number",
                "Value": self.__a_number
            },
            {
                "Key": "email",
                "Value": self.__email
            }
        ]
        
        response = iam_client.create_user(UserName=self.__username, Tags=tags)
        iam_client.create_login_profile(UserName=self.__username, Password=self.__password, PasswordResetRequired=True)
        iam_client.add_user_to_group(GroupName=STUDENT_GROUP_NAME, UserName=self.__username)
        print(f"Created user: {self.__username}")
        
        self.__user_arn = response["User"]["Arn"]
        
        
    def create_cloud9_env(self):
        """
        Create a cloud9 environment on a t2.micro instance that belongs
        to the user
        """
        cloud9_client = boto3.client("cloud9")
        print("\n"+self.__user_arn)
        response = cloud9_client.create_environment_ec2(
            name=f'{self.__first_name}-{self.__last_name}-{self.__course}',
            instanceType='t2.micro',
            automaticStopTimeMinutes=30,
            ownerArn=self.__user_arn,
            connectionType='CONNECT_SSH')
            
        self.__cloud9_env_id = response["environmentId"]
        print("created environment")
            
        
    def share_env(self, user_arn):
        """
        Share the user's cloud9 environment with the given user_arn
        """
        cloud9_client = boto3.client("cloud9")
        
        cloud9_client.create_environment_membership(
            environmentId=self.__cloud9_env_id,
            userArn=user_arn,
            permissions='read-write')
        print("shared environment")