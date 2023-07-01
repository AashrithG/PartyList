from flask import Flask, render_template, request, redirect, url_for, flash
from utilties.authentication import hash_password
from flask_sqlalchemy import SQLAlchemy
import click
from utilties.generator import attendees
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user

app = Flask(__name__)

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

@app.before_first_request
def create_database():
     db.create_all()

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
            return "Success"
        else:
            return "Failure"
    return render_template('login.html')

@app.route('/logout')
def logout():
    """This route logs out the user"""
    logout_user()
    return "You are logged out"

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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)