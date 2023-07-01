from passlib.hash import pbkdf2_sha256 # Algorithm used
import json

def create_user(username:str, password:str):
    """ Function to create a username and password """
    password = pbkdf2_sha256.hash(password)
    result = {'username': username, 'password': password}
    print(result)

def verify_user(username:str, password:str):
    """ Function to verify a users password """
    hash = '$pbkdf2-sha256$29000$fI/x/t8751wLwZgTYsy51w$1Tkf6zmf6JK9KYCKp/09udAYsakvsTqKlOOXc2zoEuk'
    result = pbkdf2_sha256.verify(password, hash)
    print(result)

def hash_password(password:str):
    password = pbkdf2_sha256.hash(password)
    # returning the password for the create_user function
    return password

loop = 0

'''
# verify username and password
while loop == 0:
    password = input("Type: ")
    if verify_user(username='aashrith', password=password) == True:
        exit()
    else:
        pass
'''