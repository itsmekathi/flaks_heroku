from . import api
from flask import request, flash, jsonify
from app import db
from app.models import ToDoList


@api.route('/todo_list/<int:todo_list_id>', methods=["GET", "DELETE"])
def todolists(todo_list_id):
    todo_list = ToDoList.query.get_or_404(todo_list_id)
    if request.method == "GET":
        return jsonify(todo_list.to_json())
    if request.method == "DELETE":
        db.session.delete(todo_list)
        db.session.commit()
        return jsonify({'status': 'deleted'})
