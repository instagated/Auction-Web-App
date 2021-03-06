from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from .models import User
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)


# Login function
@bp.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        #get the username and password from the database
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        #if there is no user with that name
        if u1 is None:
            error='There is no such username registered! Try registering below.'
        #check the password - notice password hash function
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password!'
        if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            flash(error, 'danger')
    return render_template('user.html', form=login_form, heading='Login')

# Register function
@bp.route('/register', methods=['GET','POST'])
def register():
    register = RegisterForm()
    #the validation of form submit is fine
    if (register.validate_on_submit() == True):
            #get username, password, email, contact number and address from the form
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            contact_num=register.contact_number.data
            user_address=register.address.data

            #check if a user exists
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            # don't store the password - create password hash
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email, contact_no=contact_num, addr=user_address)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')

# Logs user out if current logged in
@bp.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'warning')
    return redirect(url_for('auth.login'))
