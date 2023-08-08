import boto3
import string
import random
from constants import STUDENT_GROUP_NAME, STUDENT_IAM_SUBSTRING


def user_factory(first_name: str, last_name: str, a_number: str, email: str, section: str) -> dict:
    """
    Given a single student's information, create an IAM user for the student, create a login profile,
    and add the user to the DATA3500-5500-students policy group.

    Returns JSON containing the created user's information, as stored in AWS.

    :param first_name: the student's first name. Used to create the username
    :param last_name: the student's last name. Used to create the username.
    :param a_number: the student's A-Number. Added to the user as a tag.
    :param email: the student's email. Added to the user as a tag.
    :return user_details: returns dict containing information necessary to send credentials
    """
    iam_client = boto3.client("iam")

    # creating the user
    tags = [
            {
                "Key": "a_number",
                "Value": a_number.lower()
             },
            {
                "Key": "email",
                "Value": email
             }
            ]

    # for the event two students have the same fname and lname
    try:
        user_creation_response = iam_client.create_user(UserName=first_name.lower() + "." + last_name.lower() + STUDENT_IAM_SUBSTRING, Tags=tags)
    except iam_client.exceptions.EntityAlreadyExistsException:
        user_creation_response = iam_client.create_user(UserName=first_name.lower() + "." + last_name.lower() + STUDENT_IAM_SUBSTRING + "-1", Tags=tags)

    # create login profile
    password = "A@1f"+(''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
    iam_client.create_login_profile(UserName=user_creation_response["User"]["UserName"], Password=password, PasswordResetRequired=True)

    # add user to group
    iam_client.add_user_to_group(GroupName=STUDENT_GROUP_NAME, UserName=user_creation_response["User"]["UserName"])

    # getting user details
    user_details = iam_client.get_user(UserName=user_creation_response["User"]["UserName"])
    user_details["User"]["Password"] = password
    user_details["User"]["FirstName"] = first_name
    user_details["User"]["Email"] = email
    user_details["User"]["Section"] = section
    
    print(f"Created user: {user_details['User']['UserName']}")
    return user_details


if __name__ == "__main__":
    """
    creating a test student
    """
    print(user_factory(first_name="test", last_name="student", a_number="a12345678", email="test.student@notreal.com", section="DATA-5500-IO1"))
