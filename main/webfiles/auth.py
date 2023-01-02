from flask import Blueprint, render_template, request, redirect, flash

auth = Blueprint('auth', __name__)

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
            flash("Account created", category="Success")
            return redirect('/')
        else:    
            return render_template("sign_up.html")
