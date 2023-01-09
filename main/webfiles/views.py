from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from . import models, db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('home.html', user=current_user)
    else:
        data = request.form
        if len(data['note']) >= 1:
            new_note = models.Note(
                text = data['note'],
                user_id = current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            flash("Note was created successfully.", category='Success')
        else:
            flash("You need to type something.", category='Error')

        return render_template('home.html', user=current_user)


@views.route('/delete/', methods=['POST',])
@login_required
def delete():
    if request.method == 'POST':
        note_id = request.form.get('note_id')
        note = models.Note.query.filter_by(id=note_id, user_id=current_user.id).first()

        db.session.delete(note)
        db.session.commit()
        flash("Note was deleted successfully", category='Success')
        return redirect(url_for('views.index'))
