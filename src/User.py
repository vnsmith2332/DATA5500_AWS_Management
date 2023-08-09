import boto3
import string
import random
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
        
        iam_client.create_user(UserName=self.__username, Tags=tags)
        iam_client.create_login_profile(UserName=self.__username, Password=self.__password, PasswordResetRequired=True)
        iam_client.add_user_to_group(GroupName=STUDENT_GROUP_NAME, UserName=self.__username)
        print(f"Created user: {self.__username}")
        
        
    def send_credentials(self):
        ses_client = boto3.client("ses")
        
        subject = f"{self.__course} AWS Credentials"
        body = f"Hi {self.__first_name.capitalize()},\n\nWelcome to {self.__course}! We're excited to have you in the course and can't wait to get to know you better!\n\nThis course utilizes the cloud platform Amazon Web Services (AWS) and its IDE, Cloud9. In order to allow you to access this service, we have created an account for you. All the information you need to sign in can be found below:\n\nLogin Page: https://{AWS_ROOT_ACCT_ID}.signin.aws.amazon.com/console\nUsername: {self.__username}\nPassword: {self.__password}\n\nAfter you access your account, you will be prompted to reset your password; please choose a secure password and do not share it with others. Your professor will provide further instructions on how to setup your Cloud9 environment. If you have any trouble logging in, please reach out to the professor and/or TAs.\n\nAgain, welcome to the course! Here's to a great semester!\n\nDATA 3500/5500 Team"
        
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={
                'ToAddresses': [
                    self.__email
                ]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        
        print(f"Sent credentials for {self.__username} to {self.__email}\n")
        