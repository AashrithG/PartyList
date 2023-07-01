'''
This program will check if a password is strong or not.
It will be in a function.
'''

# the function to check to password
def check(password:str):
    if len(password) >= 8 and password.upper() != password and password.lower() != password:
        try:
            int(password)
        except:
            print("strong password")
    else:
        print("weak password")

password = input("Enter password: ")
check(password=password)