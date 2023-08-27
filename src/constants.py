# substring to identify student users and resources
# TODO: make "-DATA-500" --> ".DATA-500"
STUDENT_IAM_SUBSTRING = ".DATA-500"
# name of group to which all students are added
STUDENT_GROUP_NAME = "DATA3500-5500-students"
# email to send credentials from
SENDER_EMAIL = "victor.smith@usu.edu"
# acct ID for login link
AWS_ROOT_ACCT_ID = "141016442588"
# max emails per second allotted by SES
MAX_SEND_RATE = 14
# course numbers for student emails, to be determined by parsing section name
COURSES = {
    "3500": "DATA-3500",
    "5500": "DATA-5500",
    "6500": "DATA-6500"
}
# beginning password for all students
PASSWORD = "H8P+0Ar1@"
# grader and root user ARNs for TA/professor access to environments
ROOT_ARN = "arn:aws:iam::141016442588:root"
GRADER_ARN = "arn:aws:iam::141016442588:user/victorsmith"
