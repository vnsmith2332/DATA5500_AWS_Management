import sys
from emailer import *
from user_factory import *
from user_nuke import *
from usage import usage


def main():
    # check for required args at command line
    if len(sys.argv) < 2:
        usage()

    create_or_destroy = 0
    while create_or_destroy not in ["1", "2"]:
        create_or_destroy = input("Would you like to...\n\t1) Create student IAM users\n\t2) Destroy all student IAM users and their resources\n")
        if create_or_destroy not in ["1", "2"]:
            print("Invalid selection.")

    with open(sys.argv[1]) as f:
        f.readline()
        if create_or_destroy == "1":
            for line in f:
                line = line.strip().lower()
                values = line.split(",")
                user_info = user_factory(first_name=values[0], last_name=values[1], a_number=values[2], email=values[3])
                send_credentials(user_details=user_info)
            print("All users created successfully!")

        else:
            nuke_environments()
            nuke_users()
            print("All student users and their resources have been deleted/terminated.")


if __name__ == "__main__":
    main()
