def usage(error="", additive=""):
    """
    Unified interface for error messages
    
    :param error: the type of error the user made
    :param additive: any information from the user's input that should be included in the error message
    """
    if error == "invalid_option":
        print(f"python src/main.py UTILITY [STUDENT_DATA_FILE.csv]\n\nERROR: '{additive}' is an invalid option for UTILITY. Use either 'create' or 'destroy'.\n")
        
    elif error == "insufficient_args":
        print(f"python src/main.py UTILITY [STUDENT_DATA_FILE.csv]\n\nERROR: the 'create' option requires the additional positional argument STUDENT_DATA_FILE.csv")
            
    else:
        print("USAGE: python src/main.py UTILITY [STUDENT_DATA_FILE.csv]\n\nCreate IAM users for students with information from a data file OR destroy IAM users and resources associated with students\n\t- UTILITY: functionality of the program you would like to use.\n\t\t- 'create': option to create IAM users. Requires the follow up argument STUDENT_DATA_FILE.csv when invoked.\n\t\t- 'destroy': option to destroy IAM users and their resources.\n\t- STUDENT_DATA_FILE.csv: a file containing the requisite information to create and share a student IAM user. Required if the 'create' option is invoked.\n")
    exit()
    