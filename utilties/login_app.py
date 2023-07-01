'''
This program will be a GUI that will let the user create an account and login.
This program will use the tkinter module.
This program will use functions from other programs.
This program will use a database to check the account on write a new user to it.
'''

# importing tkinter and its submodule themed widgets to make the GUI
from tkinter import *
from tkinter import ttk

# importing login and sign up functions
from sign_up import create_user
from sign_in import check

# login function that the button calls
def login():
    Email = email.get()
    Password = password.get()
    check(email=Email, password=Password)

# making the main application window
root = Tk()
# naming the main window
root.title("Login App")
# setting a geometry to the window
root.geometry("400x300")

# this frame holds the contents
contents = ttk.Frame(master = root)
contents.pack()

# this is a label that says login as a heading
heading = ttk.Label(contents, text = "Login", font = "24")
heading.pack(pady=20)

# this is where the email can be entered by the user
email = ttk.Entry(contents)
email.pack(pady=10)

# this is where the password can be entered by the user
password = ttk.Entry(contents)
password.pack(pady=10)

# this is the button that calls the function that checks the account
login = ttk.Button(contents, text="Login", command=login)
login.pack(pady=10)

# this is a text box that tells the user

# making the mainloop so that the window appears to the user
root.mainloop()