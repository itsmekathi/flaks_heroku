from flask import abort, flash, jsonify, redirect, render_template, url_for, abort, request
from flask_login import current_user, login_required

from app import db
from app.models import PersonalJournal, User

from . import journal
from .forms import EditJournalForm, NewJournalForm


@login_required
@journal.route('', methods=["GET", "POST"])
def index():
    form = NewJournalForm()
    if form.validate_on_submit():
        personal_journal = PersonalJournal(
            tag_line=form.tag_line.data, body_html=form.body.data, is_private=form.is_private.data)
        db.session.add(personal_journal)
        db.session.commit()
        return redirect(url_for('journal.index'))

    page = request.args.get('page', 1, type=int)
    pagination = PersonalJournal.query.order_by(
        PersonalJournal.created_on.desc()).paginate(page, 5, error_out=False)
    return render_template('journal/index.html', form=form, pagination=pagination)


@login_required
@journal.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    journals = user.journals.orderby(PersonalJournal.created_on.desc()).all()
    return render_template('journal/user.html', user=user, journals=journals)


@login_required
@journal.route('/<int:id>')
def journalbyid(id):
    return "hellow"


@login_required
@journal.route('/edit/<int:id>')
def editbyid(id):
    return "edit"
