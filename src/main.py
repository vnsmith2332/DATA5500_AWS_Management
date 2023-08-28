import sys
from time import sleep

from user_nuke import *
from constants import MAX_SEND_RATE, ROOT_ARN, GRADER_ARN
from usage import usage
from User import User


def main():
    # check for required args at command line
    if len(sys.argv) < 2:
        usage()
        
    # destroy users
    elif sys.argv[1].lower().strip() == "destroy":
        print("You are about to destroy all IAM users and resources in all DATA X500 courses. All data contained in these resources will be lost. This cannot be undone. Would you like to proceed? [y/n] > ", end="")
        proceed = input()
        if proceed.lower() == "y":
            nuke_environments()
            nuke_users()
            print("All student users and their resources have been deleted/terminated.")
        else:
            print("Process terminated. No resources were effected.")
            exit()
    
    # create users      
    elif sys.argv[1].lower() == "create":
        if len(sys.argv) < 3:
            usage(error="insufficient_args")
            
        # create a user for each student in the file
        with open(sys.argv[2]) as f:
            f.readline()
            users = []
            for line in f:
                line = line.strip().lower().replace(" ", "")
                values = line.split(",")
                user = User(first_name=values[2], last_name=values[1], a_number=values[3], email=values[4], section=values[5])
                user.create_user()
                users.append(user)
                
        # sleep to allow users to sync in AWS
        sleep(30)
        
        # provision environments for each user
        for user in users:
            user.create_cloud9_env()
            user.share_env(user_arn=ROOT_ARN)
            user.share_env(user_arn=GRADER_ARN)
        print("All users created successfully!")
            
    else:
        usage(error="invalid_option", additive=sys.argv[1])
            

if __name__ == "__main__":
    main()
