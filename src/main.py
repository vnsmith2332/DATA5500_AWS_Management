import sys
from time import sleep

from emailer import *
from user_factory import *
from user_nuke import *
from constants import MAX_SEND_RATE
from usage import usage


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
        with open(sys.argv[2]) as f:
            f.readline()
            emails_sent = 0
            for line in f:
                # limit send rate to MAX_SEND_RATE emails per second
                if emails_sent % MAX_SEND_RATE == 0:
                    sleep(1)
                line = line.strip().lower().replace(" ", "")
                values = line.split(",")
                user_info = user_factory(first_name=values[2], last_name=values[1], a_number=values[3], email=values[4], section=values[5])
                send_credentials(user_details=user_info)
                emails_sent += 1
            print("All users created successfully!")
            
    else:
        usage(error="invalid_option", additive=sys.argv[1])
            

if __name__ == "__main__":
    main()
