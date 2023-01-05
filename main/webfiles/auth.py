from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

from . import models

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", text="samyar")
    else:
        data = request.form
        print(data)
        return redirect('/login/')
@auth.route('/logout/')
def logout():
    return "Logout page"

@auth.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("sign_up.html")
    else:
        error = False
        data = request.form

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

            flash("Account created", category="Success")
            return redirect(url_for('views.index'))
        else:    
            return render_template("sign_up.html")
