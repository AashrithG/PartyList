'''
This program will let the user sign up.
It will store the password securely.
It will use the passlib module to encrypt the password.
It will store the information in a sqlite3 database.
It will ask for an username and a password.
'''

# importing the passlib module to encrypt the password
from passlib.hash import pbkdf2_sha256

# importing sqlite3 to access the database
import sqlite3

# this function will encrypt a password
def encrypt(password:str):
    # hashing/encrypting the password
    password = pbkdf2_sha256.hash(password)
    # returning the password for the create_user function
    return password


# this function will create an user in the database
def create_user(username:str, password:str):
    # connecting to the sqlite3 database
    con = sqlite3.connect("accounts.db")

    # creating a cursor to execute SQL statments and queries
    cursor = con.cursor()
    # creating a table (if one doesn't exist)
    try:
        cursor.execute("CREATE TABLE accounts(username, password)")
    except:
        pass
    # this is the hashed password
    psword = encrypt(password=password)
    # inserting the username and password into the database
    cursor.execute(f"""
    INSERT INTO accounts VALUES
        ('{username}', '{psword}')
    """)
    # commit the change to the database
    con.commit()
    # closing the connection with the database
    con.close()
