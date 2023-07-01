from sign_up import create_user
from sign_in import check

choice = input("Login or Sign Up (l/s): ")

if choice == 'l':

    print("logining in")
    email = input("Email: ")
    password = input("Password: ")
    check(email=email, password=password)

elif choice == 's':

    print("signing up")
    email = input("Email: ")
    password = input("Password: ")
    create_user(email=email, password=password)

else:
    print("problem in choice")