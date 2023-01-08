from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

from . import models

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", user=current_user)
    else:
        data = request.form
        user = models.User.query.filter_by(email=data['email']).first()
        if user:
            if check_password_hash(user.password, data['password']):
                login_user(user=user, remember=True)
                flash("Logged in successfully. Welcome back!", category='Success')
                return redirect(url_for('views.index'))
            else:
                flash("Email or password is incorrect. Try again", category='Error')
            return redirect(url_for('auth.login'))
        else:
            flash("User not found", category='Error')
            return redirect(url_for('auth.login'))

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("sign_up.html", user=current_user)
    else:
        error = False
        data = request.form
        if models.User.query.filter_by(email=data['email']).first():
            flash("A user with this email already exists, try another one", category='Error')
            error = True

        if len(data['email']) < 4:
            flash("Email is too short", category='Error')
            error = True

        if len(data['password1']) < 4:
            flash("Choose a longer password", category='Error')
            error = True

        if data['password1'] != data['password2']:
            flash("Your password is not same as confirmed one", category='Error')
            error = True

        if error == False:
            new_user = models.User(
                email= data['email'],
                first_name = data['firstName'],
                last_name = data['lastName'],
                password = generate_password_hash(data['password1'], method='sha256')
                )
            db.session.add(new_user)
            db.session.commit()


            login_user(user=new_user, remember=True)
            flash("Account created", category="Success")
            return redirect(url_for('views.index'))
        else:    
            return render_template("sign_up.html")
