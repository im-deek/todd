
# // Any functions I think will be repeated over various commands will be in here for easy code reusability. //

def determineAuth(user_id):

    # // Very basic, just reads from the auth file and returns the boolean value. //

    with open("authorised_users.txt","r") as file:
        if user_id in file.read().splitlines():
            return True
        else:
            return False