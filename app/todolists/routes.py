from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import ToDoList, ToDoItem, TaskStatusLu, TaskPriorityLu, TaskUrgencyLu, ToDoItemComments, ToDoItemWorkLog
from .forms import ToDoListForm, TaskLuForm, ToDoItemForm, ToDoItemEditForm, ToDoItemLogWorkForm
from . import todolists
from datetime import date, datetime


@todolists.route('/status', methods=['GET', 'POST'])
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
        flash('New status has been added', 'success')
    statuses = TaskStatusLu.query.all()
    return render_template('/todolists/lookups.html', form=form, lookups=statuses, legend='Add New Status', lookupTitle='Status')


@todolists.route('/status/edit/<int:status_id>', methods=['GET', 'POST'])
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


@todolists.route('/status/delete/<int:status_id>', methods=['POST'])
@login_required
def delete_status(status_id):
    status = TaskStatusLu.query.get_or_404(status_id)
    db.session.delete(status)
    db.session.commit()
    flash('The status has been deleted', 'success')
    return redirect(url_for('todolists.status'))


@todolists.route('/priority', methods=['GET', 'POST'])
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


@todolists.route('/priority/edit/<int:priority_id>', methods=['GET', 'POST'])
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


@todolists.route('/priority/delete/<int:priority_id>', methods=['POST'])
@login_required
def delete_priority(priority_id):
    priority = TaskPriorityLu.query.get_or_404(priority_id)
    db.session.delete(priority)
    db.session.commit()
    flash('The priority has been deleted', 'success')
    return redirect(url_for('todolists.priority'))


@todolists.route('/urgency', methods=['GET', 'POST'])
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


@todolists.route('/urgency/edit/<int:urgency_id>', methods=['GET', 'POST'])
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


@todolists.route('/urgency/delete/<int:urgency_id>', methods=['POST'])
@login_required
def delete_urgency(urgency_id):
    urgency_data = TaskUrgencyLu.query.get_or_404(urgency_id)
    db.session.delete(urgency_data)
    db.session.commit()
    flash('The Urgency has been deleted', 'success')
    return redirect(url_for('todolists.urgency'))


@todolists.route('/new', methods=['GET', 'POST'])
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


@todolists.route('/', methods=['GET'])
@login_required
def all_todolist():
    # Get the query parameters
    todo_lists = ToDoList.query.filter_by(user=current_user).order_by('title')
    return render_template('/todolists/todolists.html', todo_lists=todo_lists, title=f"All To-Do Lists")


@todolists.route('/delete/<int:todolist_id>', methods=['POST'])
@login_required
def delete_todolist(todolist_id):
    todo_list = ToDoList.query.get_or_404(todolist_id)
    if todo_list.user != current_user:
        return abort(403)
    db.session.delete(todo_list)
    db.session.commit()
    flash('Todo list has been deleted')
    return redirect(url_for('todolists.all_todolist'))


@todolists.route('/<int:todolist_id>', methods=['GET'])
@login_required
def todolist_details(todolist_id):
    # Get the query parameters
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pagesize', 5, type=int)

    todo_list = ToDoList.query.get_or_404(todolist_id)
    if todo_list.user != current_user:
        return abort(403)
    todo_items = ToDoItem.query.filter_by(todo_list_id=todolist_id).order_by(
        ToDoItem.scheduled_date).paginate(page=page, per_page=page_size)
    return render_template('/todolists/todolist_details.html', title=f"To-Do List: {todo_list.title}", todo_items=todo_items, todo_list=todo_list)


@todolists.route('/<int:todolist_id>/todoitems', methods=['POST', 'GET'])
@login_required
def todoitem_new(todolist_id):
    todo_list = ToDoList.query.get_or_404(todolist_id)
    form = ToDoItemForm()
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
                comment=form.comment.data, user=current_user)
            todo_item.comments.append(comment)
        db.session.add(todo_item)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('todolists.todolist_details', todolist_id=todolist_id))
    # Initialize the scheduled date to today on get request
    form.scheduled_date.data = date.today()
    return render_template('/todolists/todo_item.html', title=f'New To-Do Item', form=form, legend='New To-Do Item')


@todolists.route('/todoitems/edit/<int:todoitem_id>', methods=['POST', 'GET'])
@login_required
def edit_todoitem(todoitem_id):
    todo_item = ToDoItem.query.get_or_404(todoitem_id)
    if todo_item.todolist.user != current_user:
        abort(403)
    form = ToDoItemEditForm()
    log_workform = ToDoItemLogWorkForm()
    form.status_id.choices = [(status.id, status.name)
                              for status in TaskStatusLu.query.order_by('name').all()]
    form.priority_id.choices = [(priority.id, priority.name)
                                for priority in TaskPriorityLu.query.order_by('name').all()]
    form.urgency_id.choices = [(urgency.id, urgency.name)
                               for urgency in TaskUrgencyLu.query.order_by('name').all()]

    if form.is_submitted() and form.validate_on_submit():
        todo_item.title = form.title.data
        todo_item.description = form.description.data
        todo_item.status_id = form.status_id.data
        todo_item.priority_id = form.priority_id.data
        todo_item.urgency_id = form.urgency_id.data
        todo_item.scheduled_date = form.scheduled_date.data
        todo_item.estimated_duration_hours = form.estimated_duration_hours.data
        todo_item.estimated_duration_minutes = form.estimated_duration_minutes.data
        if form.comment.data is not None:
            comment = ToDoItemComments(
                comment=form.comment.data, user=current_user, todoitem=todo_item)
            db.session.add(comment)
        db.session.add(todo_item)
        db.session.commit()
        flash('Todo-Item has been updated', 'success')
        return redirect(url_for('todolists.todolist_details', todolist_id=todo_item.todo_list_id))
    if log_workform.is_submitted() and log_workform.validate_on_submit():
        work_log = ToDoItemWorkLog(todoitem=todo_item, start_datetime=log_workform.start_datetime.data,
                                   end_datetime=log_workform.end_datetime.data, comment=log_workform.comment.data, user=current_user)
        db.session.add(work_log)
        db.session.commit()
        flash('Your worklog has been recorded', 'success')
        return redirect(url_for('todolists.todolist_details', todolist_id=todo_item.todo_list_id))
    form.title.data = todo_item.title
    form.description.data = todo_item.description
    form.scheduled_date.data = todo_item.scheduled_date
    form.estimated_duration_hours.data = todo_item.estimated_duration_hours
    form.estimated_duration_minutes.data = todo_item.estimated_duration_minutes
    form.status_id.data = todo_item.status_id
    form.priority_id.data = todo_item.priority_id
    form.urgency_id.data = todo_item.urgency_id
    log_workform.start_datetime.data = datetime.now()
    log_workform.end_datetime.data = datetime.now()
    return render_template('/todolists/todo_item.html', title=f'Edit Item: {todo_item.title} ', form=form, log_workform=log_workform, legend='Edit/Update To-Do Item')


@todolists.route('/todoitems/delete/<int:todoitem_id>', methods=['POST', 'GET'])
@login_required
def delete_todoitem(todoitem_id):
    todo_item = ToDoItem.query.get_or_404(todoitem_id)
    if todo_item.todolist.user != current_user:
        abort(403)
    todolist_id = todo_item.todolist.id
    db.session.delete(todo_item)
    db.session.commit()
    flash('The task has been deleted.', 'success')
    return redirect(url_for('todolists.todolist_details', todolist_id=todolist_id))
