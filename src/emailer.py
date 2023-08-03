import boto3

def send_credentials(user_details: dict):
    """
    Given a dictionary containing an IAM user's information, send the login information to the
    associated student's email
    """
    SENDER_EMAIL = "data5500.credentials@gmail.com"
    AWS_ROOT_ACCT_ID = "410215147971"

    recipient_email = user_details["User"]["Email"]
    username = user_details["User"]["UserName"]
    password = user_details["User"]["Password"]
    fname = user_details["User"]["FirstName"]

    subject = "DATA 3500/5500 AWS Login Credentials"
    body = f"Hi {fname.capitalize()},\n\nWelcome to DATA 3500/5500! We're excited to have you in the course and can't wait to get to know you better!\n\nThis course utilizes the cloud platform Amazon Web Services (AWS) and its IDE, Cloud9. In order to allow you to access this service, we have created an account for you. All the information you need to sign in can be found below:\n\nLogin Page: https://{AWS_ROOT_ACCT_ID}.signin.aws.amazon.com/console\nUsername: {username}\nPassword: {password}\n\nAfter you access your account, you will be prompted to reset your password; please choose a secure password and do not share it with others. Your professor will provide further instructions on how to setup your Cloud9 environment. If you have any trouble logging in, please reach out to the professor and/or TAs ASAP!\n\nPlease do not respond to this email or attempt to get assistance via this email address. The address is not monitored and all mail is deleted automatically.\n\nAgain, welcome to the course! Here's to a great semester!\n\nDATA 3500/5500 Team"
    ses_client = boto3.client("ses")
    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [
                recipient_email
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


if __name__ == "__main__":
    """
    Send a test email to a test student; user details are arbitrary
    """
    user_details = {"User":
                        {"Email": "vnsmith2332@gmail.com",
                         "UserName": "victor.smith",
                         "Password": "password123",
                         "FirstName": "Victor"
                         }
                    }

    send_credentials(user_details)
