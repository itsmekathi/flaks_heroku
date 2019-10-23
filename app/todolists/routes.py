from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import ToDoList, ToDoItem
from .forms import ToDoListForm

todolists = Blueprint('todolists', __name__)

@todolists.route('/todolists/new', methods=['GET','POST'])
def new_todolist():
    form = ToDoListForm()
    if form.validate_on_submit():
        todolist = ToDoList(title = form.title.data,
        description= form.description.data, user= current_user)
        db.session.add(todolist)
        db.session.commit()
        flash('Your new todo-list has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('/todolists/create_todolist.html', title="New ToDoList", form = form, legend='New ToDoList')


