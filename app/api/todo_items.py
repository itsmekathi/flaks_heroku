from . import api
from flask import request, flash, jsonify
from app import db
from app.models import ToDoItem, ToDoList, User
from app.api.errors import unauthorized
from flask_login import current_user
from .authentication import auth


@api.route('/todo_item/<int:todo_item_id>', methods=["GET", "DELETE"])
def todoitems(todo_item_id):
    todo_item = ToDoItem.query.get_or_404(todo_item_id)
    if request.method == "GET":
        return jsonify(todo_item.to_json())
    if request.method == "DELETE":
        db.session.delete(todo_item)
        db.session.commit()
        return jsonify({'status': 'deleted'})

@api.route('/todo_item/move', methods=["PUT"])
def move_todoitem():
    request_data = request.get_json()
    todo_list_id = int(request_data["todoListId"])
    todo_item_id = int(request_data["todoItemId"])
    todo_list = ToDoList.query.get_or_404(todo_list_id)
    user_or_email = auth.username()
    user = User.query.filter((User.email == user_or_email) | (
        User.username == user_or_email)).first()
    if todo_list.user != user:
        return unauthorized('You donot have access to this list')
    todo_item = ToDoItem.query.get_or_404(todo_item_id)
    todo_item.todo_list_id = todo_list.id
    db.session.add(todo_item)
    db.session.commit()
    return jsonify({'status':'success'})
