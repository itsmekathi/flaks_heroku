from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import ToDoList, ToDoItem, TaskStatusLu, TaskPriorityLu, TaskUrgencyLu, ToDoItemComments
from .forms import ToDoListForm, TaskLuForm, NewToDoItemForm
from . import todolists


@todolists.route('/todolists/status', methods=['GET', 'POST'])
@login_required
def status():
    form = TaskLuForm()
    if form.validate_on_submit():
        status_data = TaskStatusLu(
            name=form.name.data, description=form.description.data, style_class=form.style_class.data)
        db.session.add(status_data)
        db.session.commit()
        form.name.data = ""
        form.description.data = ""
        form.style_class.data = ""
        flash('New status has been added')
    statuses = TaskStatusLu.query.all()
    return render_template('/todolists/lookups.html', form=form, lookups=statuses, legend='Add New Status', lookupTitle='Status')


@todolists.route('/todolists/status/edit/<int:status_id>', methods=['GET', 'POST'])
@login_required
def edit_status(status_id):
    form = TaskLuForm()
    status_data = TaskStatusLu.query.get_or_404(status_id)
    if form.validate_on_submit():
        status_data.name = form.name.data
        status_data.description = form.description.data
        status_data.style_class = form.style_class.data
        db.session.add(status_data)
        db.session.commit()
        flash('The status has been updated', 'success')
        return redirect(url_for('todolists.status'))
    if request.method == 'GET':
        form.name.data = status_data.name
        form.description.data = status_data.description
        form.style_class.data = status_data.style_class
    statuses = [status_data]
    return render_template('/todolists/lookups.html', form=form, lookups=statuses, legend='Edit Status', lookupTitle='Status')


@todolists.route('/todolists/status/delete/<int:status_id>', methods=['POST'])
@login_required
def delete_status(status_id):
    status = TaskStatusLu.query.get_or_404(status_id)
    db.session.delete(status)
    db.session.commit()
    flash('The status has been deleted', 'success')
    return redirect(url_for('todolists.status'))


@todolists.route('/todolists/priority', methods=['GET', 'POST'])
@login_required
def priority():
    form = TaskLuForm()
    if form.validate_on_submit():
        priority_data = TaskPriorityLu(
            name=form.name.data, description=form.description.data, style_class=form.style_class.data)
        db.session.add(priority_data)
        db.session.commit()
        form.name.data = ""
        form.description.data = ""
        form.style_class.data = ""
        flash('New task-priority has been added')
    priorities = TaskPriorityLu.query.all()
    return render_template('/todolists/lookups.html', form=form, lookups=priorities, legend='Add New Priority', lookupTitle='Priority')


@todolists.route('/todolists/priority/edit/<int:priority_id>', methods=['GET', 'POST'])
@login_required
def edit_priority(priority_id):
    form = TaskLuForm()
    priority_data = TaskPriorityLu.query.get_or_404(priority_id)
    if form.validate_on_submit():
        priority_data.name = form.name.data
        priority_data.description = form.description.data
        priority_data.style_class = form.style_class.data
        db.session.add(priority_data)
        db.session.commit()
        flash('The priority has been updated', 'success')
        return redirect(url_for('todolists.priority'))
    if request.method == 'GET':
        form.name.data = priority_data.name
        form.description.data = priority_data.description
        form.style_class.data = priority_data.style_class
    priorities = [priority_data]
    return render_template('/todolists/lookups.html', form=form, lookups=priorities, legend='Edit priority', lookupTitle='Priority')


@todolists.route('/todolists/priority/delete/<int:priority_id>', methods=['POST'])
@login_required
def delete_priority(priority_id):
    priority = TaskPriorityLu.query.get_or_404(priority_id)
    db.session.delete(priority)
    db.session.commit()
    flash('The priority has been deleted', 'success')
    return redirect(url_for('todolists.priority'))


@todolists.route('/todolists/urgency', methods=['GET', 'POST'])
@login_required
def urgency():
    form = TaskLuForm()
    if form.validate_on_submit():
        urgency_data = TaskUrgencyLu(
            name=form.name.data, description=form.description.data, style_class=form.style_class.data)
        db.session.add(urgency_data)
        db.session.commit()
        form.name.data = ""
        form.description.data = ""
        form.style_class.data = ""
        flash('New task-urgency has been added')
    urgencies = TaskUrgencyLu.query.all()
    return render_template('/todolists/lookups.html', form=form, lookups=urgencies, legend='Add New Urgency', lookupTitle='Urgency')


@todolists.route('/todolists/urgency/edit/<int:urgency_id>', methods=['GET', 'POST'])
@login_required
def edit_urgency(urgency_id):
    form = TaskLuForm()
    urgency_data = TaskUrgencyLu.query.get_or_404(urgency_id)
    if form.validate_on_submit():
        urgency_data.name = form.name.data
        urgency_data.description = form.description.data
        urgency_data.style_class = form.style_class.data
        db.session.add(urgency_data)
        db.session.commit()
        flash('The Urgency has been updated', 'success')
        return redirect(url_for('todolists.urgency'))
    if request.method == 'GET':
        form.name.data = urgency_data.name
        form.description.data = urgency_data.description
        form.style_class.data = urgency_data.style_class
    urgencies = [urgency_data]
    return render_template('/todolists/lookups.html', form=form, lookups=urgencies, legend='Edit urgency', lookupTitle='Urgency')


@todolists.route('/todolists/urgency/delete/<int:urgency_id>', methods=['POST'])
@login_required
def delete_urgency(urgency_id):
    urgency_data = TaskUrgencyLu.query.get_or_404(urgency_id)
    db.session.delete(urgency_data)
    db.session.commit()
    flash('The Urgency has been deleted', 'success')
    return redirect(url_for('todolists.urgency'))


@todolists.route('/todolists/new', methods=['GET', 'POST'])
@login_required
def new_todolist():
    form = ToDoListForm()
    if form.validate_on_submit():
        todolist = ToDoList(title=form.title.data,
                            description=form.description.data, user=current_user)
        db.session.add(todolist)
        db.session.commit()
        flash('Your new todo-list has been created!', 'success')
        return redirect(url_for('todolists.todolist_details', todolist_id=todolist.id))
    return render_template('/todolists/create_todolist.html', title="New ToDoList", form=form, legend='New ToDoList')


@todolists.route('/todolists', methods=['GET'])
@login_required
def all_todolist():
    todo_lists = ToDoList.query.filter_by(user=current_user).order_by('title')
    return render_template('/todolists/todolists.html', todo_lists=todo_lists, title=f"All To-Do Lists")


@todolists.route('/todolists/<int:todolist_id>', methods=['GET'])
@login_required
def todolist_details(todolist_id):
    todo_list = ToDoList.query.get_or_404(todolist_id)
    todo_items = ToDoItem.query.filter_by(todo_list_id=todolist_id).all()
    return render_template('/todolists/todolist_details.html', title=f"To-Do List: {todo_list.title}", todo_items=todo_items, todo_list=todo_list)



@todolists.route('/todolists/todoitems/<int:todolist_id>', methods=['POST', 'GET'])
@login_required
def todoitem_new(todolist_id):
    todo_list = ToDoList.query.get_or_404(todolist_id)
    form = NewToDoItemForm()
    form.status_id.choices = [(status.id, status.name)
                              for status in TaskStatusLu.query.order_by('name').all()]
    form.priority_id.choices = [(priority.id, priority.name)
                                for priority in TaskPriorityLu.query.order_by('name').all()]
    form.urgency_id.choices = [(urgency.id, urgency.name)
                               for urgency in TaskUrgencyLu.query.order_by('name').all()]
    if form.validate_on_submit():
        todo_item = ToDoItem(title=form.title.data,
                             description=form.description.data, status_id=form.status_id.data,
                             priority_id=form.priority_id.data, urgency_id=form.urgency_id.data,
                             todo_list_id=todolist_id, scheduled_date=form.scheduled_date.data,
                             estimated_duration_hours=form.estimated_duration_hours.data,
                             estimated_duration_minutes=form.estimated_duration_minutes.data)
        if form.comment.data is not None:
            comment = ToDoItemComments(
                comment=form.comment.data, user_id=current_user.id, user_name=current_user.username)
            todo_item.comments.append(comment)
        db.session.add(todo_item)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('todolists.todolist_details', todolist_id=todolist_id))
    return render_template('/todolists/todolist_new.html', title=f'New To-Do Item', form=form, legend='New To-Do Item')


@todolists.route('/todolists/todoitems/edit/<int:todoitem_id>', methods=['POST', 'GET'])
@login_required
def edit_todoitem(todoitem_id):
    return redirect(url_for('todolists.todolist_details', todolist_id=todoitem_id))


@todolists.route('/todolists/todoitems/delete/<int:todoitem_id>', methods=['POST', 'GET'])
@login_required
def delete_todoitem(todoitem_id):
    return redirect(url_for('todolists.todolist_details', todolist_id=todoitem_id))
