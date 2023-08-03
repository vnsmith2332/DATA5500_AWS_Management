import boto3
import string
import random

# substring to identify student users and resources
STUDENT_IAM_SUBSTRING = "DATA-500"
# name of group to which all students are added
STUDENT_GROUP_NAME = "students"


def user_factory(first_name: str, last_name: str, a_number: str, email: str) -> dict:
    """
    Given a single student's information, create an IAM user for the student, create a login profile,
    and add the user to the student policy group.

    Returns JSON containing the created user's information, as stored in AWS.

    :param first_name: the student's first name. Used to create the username
    :param last_name: the student's last name. Used to create the username.
    :param a_number: the student's A-Number. Added to the user as a tag.
    :param email: the student's email. Added to the user as a tag.
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
    password = (''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
    iam_client.create_login_profile(UserName=user_creation_response["User"]["UserName"], Password=password, PasswordResetRequired=True)

    # add user to group
    iam_client.add_user_to_group(GroupName=STUDENT_GROUP_NAME, UserName=user_creation_response["User"]["UserName"])

    # getting user details
    user_details = iam_client.get_user(UserName=user_creation_response["User"]["UserName"])
    user_details["User"]["Password"] = password
    user_details["User"]["FirstName"] = first_name
    user_details["User"]["Email"] = email

    return user_details


if __name__ == "__main__":
    """
    creating a test student
    """
    user_factory(first_name="test", last_name="student", a_number="a12345678", email="test.student@notreal.com")
