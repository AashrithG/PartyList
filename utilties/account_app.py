'''
This program will be a GUI that will collect the user's information and creates a profile.
The profile will be stored in a database.
This program will use the tkinter module.
This program will use functions from other programs.
'''

# importing tkinter to make the GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# importing the passlib module to encrypt the password
from passlib.hash import pbkdf2_sha256

# importing sqlite3 to access the database
import sqlite3

# making the main application window
root = Tk()
# naming the main window
root.title("Profile Creator")

# creating tabs
tabs = ttk.Notebook(root)
tabs.pack(pady=5, padx=5)

# creating frames
tab1 = Frame(tabs)
tab2 = Frame(tabs)
tab1.pack(fill="both", expand=1)
tab2.pack(fill="both", expand=1)

# adding tabs
tabs.add(tab1, text='Signup')
tabs.add(tab2, text='Login')

# this function will encrypt a password
def encrypt(password:str):
    # hashing/encrypting the password
    password = pbkdf2_sha256.hash(password_entry.get())
    # returning the password for the create_user function
    return password

# this function will create an user in the database
def createUser():
    # defining the variables that hold the users info
    firstName = first_name_entry.get()
    lastName = last_name_entry.get()
    age = age_spinbox.get()
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    conditions = terms_value.get()

    # connecting to the sqlite3 database
    con = sqlite3.connect("users.db")

    # creating a cursor to execute SQL statments and queries
    cursor = con.cursor()
    # creating a table if one doesn't exist
    try:
        cursor.execute("CREATE TABLE users(firstName, lastName, age, email, username, password, conditions)")
    except:
        pass
    # this is the hashed password
    psword = encrypt(password=password)
    # inserting the username and password into the database
    cursor.execute(f"""
    INSERT INTO users VALUES
        ('{firstName}', '{lastName}', '{age}', '{email}', '{username}', '{psword}', {conditions})
    """)
    # commit the change to the database
    con.commit()
    # closing the connection with the database
    con.close()
    # messagebox shows user that user was created
    messagebox.showinfo("Message", "User Created")

def check():
    # getting the username and the password
    username = username_login_entry.get()
    password = password_login_entry.get()

    # connecting to the sqlite database
    con = sqlite3.connect("users.db")

    # creating a cursor to execute SQL statments and queries
    cursor = con.cursor()
    # this gets all the usernames
    result = cursor.execute("SELECT username FROM users")
    usernames = result.fetchall()

    # this keeps track of how many times the loop is iterated
    iterations = 0
    # this checks if there is that username in the database and checks the password if there is a matching username
    for item in usernames:
        if item[0] == username:
            result = cursor.execute("SELECT password FROM users")
            pword = result.fetchall()
            # this gets the hashed password for the username
            psword = pword[iterations][0]
            # this checks the hashed version and the normal version of the password and shows if it match to the user
            verify = pbkdf2_sha256.verify(password, psword)
            # this show the user if the password is correct or incorrect
            if verify == 1:
                messagebox.showinfo("Message", "Logged in")
                exit()
            else:
                incorrect = Label(login_frame, text="Incorrect")
                incorrect.grid(row=2, column=0)
        iterations = iterations + 1
    # closing the connect with the database
    con.close()

'''The following is in the signup tab'''

# creating a big frame inside the window
signup_frame = Frame(tab1)
signup_frame.grid(row=0, column=0)

# creating a labeled frame inside the big frame that collects the user's info
info_frame = LabelFrame(signup_frame, text="General Info")
info_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# creating a label and entry for the first name
first_name_label = Label(info_frame, text="First Name")
first_name_entry = Entry(info_frame)
# creating a label and entry for the last name
last_name_label = Label(info_frame, text="Last Name")
last_name_entry = Entry(info_frame)
# creating a label and spinbox for the age
age_label = Label(info_frame, text="Age")
age_spinbox = Spinbox(info_frame, from_=0, to=150)
# creating a label and entry for the email
email_label = Label(info_frame, text="Email")
email_entry = Entry(info_frame)
# creating a label and entry for the username
username_label = Label(info_frame, text="Username")
username_entry = Entry(info_frame)
# creating a label and entry for the password
password_label = Label(info_frame, text="Password")
password_entry = Entry(info_frame, show="*")

# keeping all the widgets in info_frame using the grid method
first_name_label.grid(row=0, column=0, padx=10, pady=10)
first_name_entry.grid(row=1, column=0, padx=10, pady=10)
last_name_label.grid(row=0, column=1, padx=10, pady=10)
last_name_entry.grid(row=1, column=1, padx=10, pady=10)
age_label.grid(row=0, column=2, padx=10, pady=10)
age_spinbox.grid(row=1, column=2, padx=10, pady=10)
email_label.grid(row=2, column=0, padx=10, pady=10)
email_entry.grid(row=3, column=0, padx=10, pady=10)
username_label.grid(row=2, column=1, padx=10, pady=10)
username_entry.grid(row=3, column=1, padx=10, pady=10)
password_label.grid(row=2, column=2, padx=10, pady=10)
password_entry.grid(row=3, column=2, padx=10, pady=10)

# creating a labeled frame inside the big frame that has a terms and conditions checkbutton
terms_frame = LabelFrame(signup_frame, text="Terms & Conditions")
terms_frame.grid(row=1, column=0, padx=10, pady=10)

# this is the value from the checkbutton
terms_value = IntVar()

# creating a checkbutton that lets the user agree with the terms and conditions
terms_checkbutton = Checkbutton(terms_frame, text="I agree with the Terms & Conditions", onvalue=1, offvalue=0, variable=terms_value)

# adding the checkbutton to the terms_frame using the grid method
terms_checkbutton.grid(row=0, column=0, padx=10, pady=10)

# creating a labeled frame inside the big frame that contains the create button
button_frame = LabelFrame(signup_frame, text="Create")
button_frame.grid(row=1, column=1, padx=10, pady=10)

# to create a button
create_button = Button(button_frame, text='Create Account', width=21, command=createUser)

# adding the button to the button_frame using the grid method
create_button.grid(row=1, column=1, padx=10, pady=9)

'''The following is in the login tab'''

# creating a big frame inside the window
login_frame = Frame(tab2)
login_frame.grid(row=0, column=0)

# creating a labeled frame inside the big frame that collects the user's info
enter_frame = LabelFrame(login_frame, text="Login Information")
enter_frame.grid(row=0, column=0, padx=10, pady=10)

# creating a label and entry for the username
username_login_label = Label(enter_frame, text="Username")
username_login_entry = Entry(enter_frame, width=33)
# creating a label and entry for the password
password_login_label = Label(enter_frame, text="Password")
password_login_entry = Entry(enter_frame, width=33, show="*")

# keeping all the widgets in enter_frame using the grid method
username_login_label.grid(row=0, column=0, padx=10, pady=10)
username_login_entry.grid(row=1, column=0, padx=10, pady=10)
password_login_label.grid(row=0, column=1, padx=10, pady=10)
password_login_entry.grid(row=1, column=1, padx=10, pady=10)

# creating a labeled frame inside the big frame that contains the create button
button_login_frame = LabelFrame(login_frame, text="Login")
button_login_frame.grid(row=1, column=0, padx=10, pady=10)

# to create a button
login_button = Button(button_login_frame, text='Login', width=59, command=check)

# adding the button to the button_frame using the grid method
login_button.grid(row=0, column=0, padx=10, pady=9)

# the makes the GUI appear to the user
root.mainloop()
