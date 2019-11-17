from . import api
from flask import request, flash, jsonify, abort
from flask_login import current_user
from app import db
from app.models import ToDoList, ToDoItem, User, TaskStatusLu
from .errors import unauthorized
from .authentication import auth

"""
Fetches all the todolist beloning to the logged in user
Returns unauthorized if he is not the owner
"""
@api.route('/todo_list', methods=["GET"])
def get_todolists_foruser():
    user_or_email = auth.username()
    user = User.query.filter((User.email == user_or_email) | (
        User.username == user_or_email)).first()
    todo_lists = ToDoList.query.filter_by(user_id=user.id).all()
    return jsonify({'todolists': [todo_list.to_json() for todo_list in todo_lists]})


"""
Gets or deletes the todolist which belongs to the user
Returns unauthorized if he is not the owner
"""
@api.route('/todo_list/<int:todo_list_id>', methods=["GET", "DELETE"])
def todolists(todo_list_id):
    todo_list = ToDoList.query.get_or_404(todo_list_id)
    if todo_list.user != current_user:
        return unauthorized('You donot have access to this list')
    if request.method == "GET":
        return jsonify(todo_list.to_json())
    if request.method == "DELETE":
        db.session.delete(todo_list)
        db.session.commit()
        return jsonify({'status': 'deleted'})


"""
Gets all todo-items which belongs to the list
Returns unauthorized if he is not the owner
"""
@api.route('/todo_list/<int:todo_list_id>/items', methods=["GET"])
def getall_todoitems(todo_list_id):
    todo_list = ToDoList.query.get_or_404(todo_list_id)
    user_or_email = auth.username()
    user = User.query.filter((User.email == user_or_email) | (
        User.username == user_or_email)).first()
    if todo_list.user != user:
        return unauthorized('You donot have access to this list')
    todo_items = ToDoItem.query.filter_by(todo_list_id=todo_list_id).all()
    return jsonify({'todoitems': [todo_item.to_json() for todo_item in todo_items]})


"""
Group todo items to display in donut chart
will return an array of labels and respective data
"""
@api.route('/todo_list/<int:todo_list_id>/chart', methods=["GET"])
def get_chartdata_for_todolist(todo_list_id):
    todo_list = ToDoList.query.get_or_404(todo_list_id)
    user_or_email = auth.username()
    user = User.query.filter((User.email == user_or_email) | (
        User.username == user_or_email)).first()
    if todo_list.user != user:
        return unauthorized('You donot have access to this list')
    todo_items_group = db.session.query(TaskStatusLu.name, db.func.count(ToDoItem.id))\
        .outerjoin(ToDoItem, (TaskStatusLu.id == ToDoItem.status_id) & (ToDoItem.todo_list_id == todo_list_id))\
            .group_by(TaskStatusLu.name).order_by(TaskStatusLu.name).all()
    labels = []
    data = []
    for status, item_count in todo_items_group:
        labels.append(status)
        data.append(item_count)
    return jsonify({'chartData': {'labels': labels, 'data': data}})