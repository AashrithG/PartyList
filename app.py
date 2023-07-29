import os
from uuid import uuid1
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash
from utilties.authentication import hash_password
from flask_sqlalchemy import SQLAlchemy
import click
from utilties.generator import attendees
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user

# CONSTANTS
UPLOAD_FOLDER = "static/profile"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


app = Flask(__name__)

# CONFIGURATION
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16 MB

app.secret_key = '8b2f13e073221a2a268594462951a9bdab1ff7a6bff30761552f6c037bcb46df'

# Instantiate SQLAlchemy
db = SQLAlchemy()
# Configure the database file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SECRET_KEY"] = 'f76f8f71954e7225b8cbd78081a0b028b505a646de9eb5e2768d661fb0315a2a'
# Initialize DB
db.init_app(app)

with app.app_context():
    db.create_all()

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

# user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create our Models
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    is_attending = db.Column(db.Boolean, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # profile_pic = db.Column(db.String, nullable=True)

@app.before_first_request
def create_database():
     db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# Authentication Mechanism
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Used to register for an account """
    if request.method == 'POST':
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = hash_password(request.form["password"])
        user = User(first_name=firstname, last_name=lastname, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('User account created', category='message')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Used to login to our application """
    if request.method == 'POST':
        # email and password for the form
        email = request.form['email']
        password = request.form['password']
        # Check email in database/password
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        verify = pbkdf2_sha256.verify(password, user.password)
        if pbkdf2_sha256.verify(password, user.password) == True:
            login_user(user)
            flash("User logged in", category='message')
            return redirect(url_for('home'))
        else:
            return "Failure"
    return render_template('login.html')

@app.route('/logout')
def logout():
    """This route logs out the user"""
    logout_user()
    flash("User logged out", category='message')
    return redirect(url_for('home'))

@app.route('/protected')
@login_required
def protect():
    return render_template('protected.html')

# CRUD Routes
@app.route('/')
def home():
    """ Read """
    data = db.session.execute(db.select(Person)).scalars()
    context = data
    return render_template('read.html', context=context)

@app.route('/create', methods=['GET', 'POST'])
def create():
    """ Create Record """
    if request.method == 'POST':
        # Process the data (append to data list)
        firstname = request.form['firstname']
        age = request.form['age']
        # TODO - FIX Toggle Button
        is_attending = True
        person = Person(first_name=firstname, age=int(age), is_attending=is_attending)
        db.session.add(person)
        db.session.commit()
        flash('User created', category='message')
        return redirect(url_for('home'))
        # Redirect the page to the home page
        return 'You posted something'
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """ Update a record """
    person = db.session.execute(db.select(Person).filter_by(id=id)).scalar_one()
    if request.method == 'POST':
        print(request.form)
        first_name = request.form['firstname']
        age = request.form['age']
        is_attending = True
        person.first_name = first_name
        person.age = age
        person.is_attending = is_attending
        db.session.commit()
        flash('User updated', category='message')
        return redirect(url_for('home'))
    return render_template('update.html', person=person)  
    

@app.route('/delete/<int:id>')
def delete(id):
    """ Delete Record """
    # Select record deletion
    person = db.session.execute(db.select(Person).filter_by(id=id)).scalar_one()
    # Creates session to delete
    db.session.delete(person)
    # Delete the record
    db.session.commit()
    flash('User deleted', category='message')
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
def profile_page():
    """This is a profile page"""
    if request.method == 'POST':
        # check in the filename extension is allowed
        if 'file' not in request.files:
            return 'File not allowed'
        file = request.files['file']
        if file.filename == '':
            return 'No file submitted'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config[UPLOAD_FOLDER], filename))
            flash('File uploaded')
            return redirect(url_for('profile_page'))
    # upload form
    # create a uuid
    # combine uuid and filename
    # store filename in database
    # store file in static folder
    return render_template("profile.html")

# Custom Commands
@app.cli.command("create-user")
@click.argument("number")
def create_user(number):
    """This command will create users"""
    data = attendees(int(number))
    for item in data:
        first_name = item['first_name']
        age = item['age']
        is_attending = item['is_attending']
        person = Person(first_name=first_name, age=int(age), is_attending=is_attending)
        db.session.add(person)
        db.session.commit()
    return f"A total of {number} people created"

# Gallery
@app.route('/gallery')
def gallery():
    """Gallery page"""
    return render_template("gallery.html")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    """Upload File"""
    if request.method == 'POST':
        filename = request.files['file']
        # File is empty
        if filename.filename == '':
            return 'file is empty'
        if filename and allowed_file(filename.filename):
            myuuid = str(uuid1())
            file = f'{myuuid}-{filename.filename}'
            filename.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
            print(filename)
            return "File Uploaded"
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)