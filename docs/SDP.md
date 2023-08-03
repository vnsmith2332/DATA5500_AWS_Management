# DATA 3500/5500 AWS Management

## Analysis
Currently, the DAIS department offers two Python courses, DATA 3500 and DATA 5500. In both courses, students use the AWS
Cloud9 IDE on personal AWS accounts. Utilizing this service has several advantages:
* Students gain exposure to AWS, an in-demand skill
* There are no hardware limitations or complications; the IDE is cloud-based and can be accessed from any device with an
internet connection.
* The AWS free tier ensures students can utilize their environment for the duration of the course for free

Despite the advantages, this approach has revealed several drawbacks:
* Students must share their environments correctly with the grader. Most students
have little to no experience with AWS IAM and incorrectly create users or do not grant adequate permissions, resulting in
many wasted hours troubleshooting for instructors/TAs.
* Students have root access and permissions, allowing them to perform potentially destructive and/or costly actions (ex:
terminating a needed EC2 instance or unknowingly utilizing a costly service, for which the student will be charged)
* Instructors and TAs typically have full administrative access to students' personal accounts, posing a significant security
threat after the course is completed
* Graders must sign in to each account individually to access completed assignments, adding significantly to the amount of time
spent grading

Given these issues, we have decided to develop a new approach for the courses, one that will allow students
to use AWS in the course, while mitigating the drawbacks. A suitable solution will achieve the following:
1. Instructors and TAs - not students - will have administrative access to a single AWS account on which student resources live
2. Students will be added as IAM users with console access to the account. They will be added to a `student` group, 
which has an appropriate permissions policy attached. Some permissions students will need:
   * Creating an EC2 instance
   * Creating, accessing, and writing/running code in Cloud9 environments

   Some things students must **not** be able to do:
   * Terminate EC2 instances
   * View resources of any kind that they did not create
   * Utilize any service other than EC2 and Cloud9
3. All students and their resources should be removed from the account at the end of each semester
4. Creation/deletion of student users, credential sharing, and termination of resources should all be managed via scripts
rather than manually

### Foreseeable Challenges
Ensuring students have appropriate permissions while following the standard of least privilege will be challenging. Testing
the policy document is expected to take a considerable amount of time.

## Design

### Getting Student Data
The following information is needed to create a user for each student and communicate the credentials:
* First name
* Last name
* Email
* A-number

All of this information is easily accessible via the course roster download option in Canvas.
This option provides a `.csv` file in the following format:
```
Name, Last Name, First Name, A Number, Email, Section
Molly Alexander, Alexander, Molly, A01285286, a01285286@usu.edu, Summer 2023 DATA-5500-IO1
Colton Butler, Butler, Colton, A02286233, a02286233@usu.edu, Summer 2023 DATA-5500-IO1
Hannah Calvin, Calvin, Hannah, A02363685, a02363685@usu.edu, Summer 2023 DATA-5500-IO1
```

Some preprocessing will need to occur on each line of the file, including:
* parsing columns for needed information
* stripping spacing

In the future, we would like to explore using the Canvas API to get this information. Time constraints make this impossible for the time being.


### Creating Student IAM Users
After retrieving student data, the next task is to create users for the students. This step includes:
1. Creating an IAM user for each student. Usernames will be the following format `firstname.lastname`
2. Create a login profile for each user. This will grant access to the AWS management console.
3. Add each user to the `student` group

```python
def user_factory(first_name: str, last_name: str, a_number: str, email: str) -> bool:
    """
    Given a single student's information, create an IAM user for the student, create a login profile,
    and add the user to the student policy group.
    
    Returns JSON containing the created user's information, as stored in AWS.
    
    :param first_name: the student's first name. Used to create the username
    :param last_name: the student's last name. Used to create the username.
    :param a_number: the student's A-Number. Added to the user as a tag.
    :param email: the student's email. Added to the user as a tag.
    """
    create boto3 iam client
    tags = {"a_number": a_number,
            "email": email}
    user_creation_response = call function to create iam user(UserName=first_name+"."+last_name, Tags=[tags])
    password = generate random password
    login_profile_response = call function to create login profile(UserName=user_creation_response["UserName"], Password=password, PasswordResetRequired=True)
    group_user_response = call function to add user to group(GroupName="student", UserName=user_creation_response["UserName"])
    user_details = get_user(user_name)
    add password to user_details
    add first and last name to user_details
    return user_details    
```

### Emailing Credentials
After creating users and their login credentials, an email must be sent to each student containing their login information.
Fortunately, AWS Simple Emailing Service (SES) includes an easy-to-use API that can be used to quickly send individual
emails.

The `mail_credentials` function will accept the output from the `user_factory`, thereby obtaining all the information needed
for the message.

```python
def mail_credentials(user_details: dict):
   """
   Given a dictionary containing an IAM user's information, send the login information to the
   associated student's email
   """
    parse user_details for username, password, section, and email
    string containing subject
    string containing body
    SES API call to send email to student
```

### Deleting IAM Users
At the end of each semester, each IAM user, as well as all resources created by that user, will be deleted. First, all Cloud9
environments and their associated EC2 instances will be terminated. Then, a second pass will be made to remove all the users.

Resources and users that need to be removed will be indentified by a substring unique to students in the course. In the case of users,
this substring will be in the username. Consequently, this substring will also be available in the `ownerArn` of any resources that
should be deleted.

```python
def nuke_environments():
    """
    Delete all Cloud9 environments in the account owned by DATA 3500/5500 students.
    Also terminates the EC2 instances on which the environments are running.
    """
    create cloud9_client

    get all env ids using list_environments()
    describe all env using describe_environments(ids)
    for each account, check ownerArn for student IAM user substring
        delete env if True


def user_nuke()
    """
    Delete all IAM users that are student users
    """
    creat iam client
    
    get all users using list_users()
    if student_iam_substring in username:
        delete login profile
        remove user from student group
        delete user
```

### Main Module
The last step is to design an entry point to the program. As an initial design, the program will accept a path to a `.csv`
file containing requisite student records to either create users or remove them. Then, the user will be prompted to indicate
whether they would like to create users or destroy them.

```python
def main():
    check length of sys.argv
    get input for create or destroy
    validate input
    if create:
        create users with details in csv
    if destroy:
        destroy users
```
## Implementation
Some notes on implementation:
* Added exception handling to `user_factory()` to handle the case that two students exist with the same first and last name
* Added an arbitrary fixed substring to the beginning of each password to ensure the password satisfies the account's password requirements
* Removal from SES sandbox must be requested to send emails to unverified addresses
* Added `src/constants.py` to store all constants needed by other files. This provides a central location where these can be easily updated if needed.

## Testing


## Deployment