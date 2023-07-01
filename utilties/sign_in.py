'''
This program will let the user sign in.
The account will be in a database that this program will access.
'''

# importing the sqlite3 module to access the database
import sqlite3

# importing the passlib module to verify the password
from passlib.hash import pbkdf2_sha256

# this function will check if the password is a match with the hashed version
def check(username:str, password:str):
    # connecting to the sqlite database
    con = sqlite3.connect("accounts.db")

    # creating a cursor to execute SQL statments and queries
    cursor = con.cursor()
    # this gets all the usernames
    result = cursor.execute("SELECT username FROM accounts")
    usernames = result.fetchall()

    # this keeps track of how many times the loop is iterated
    iterations = 0
    # this checks if there is that username in the database and checks the password if there is a matching username
    for item in usernames:
        if item[0] == username:
            result = cursor.execute("SELECT password FROM accounts")
            pword = result.fetchall()
            # this gets the hashed password for the username
            psword = pword[iterations][0]
            # this checks the hashed version and the normal version of the password and shows if it match to the user
            verify = pbkdf2_sha256.verify(password, psword)
            print("Correct")
            exit()
        iterations = iterations + 1
    # closing the connect with the database
    con.close()