from . import api
from flask import request, flash, jsonify
from app import db
from app.models import ToDoItem


@api.route('/todo_item/<int:todo_item_id>', methods=["GET", "DELETE"])
def todoitems(todo_item_id):
    todo_item = ToDoItem.query.get_or_404(todo_item_id)
    if request.method == "GET":
        return jsonify(todo_item.to_json())
    if request.method == "DELETE":
        db.session.delete(todo_item)
        db.session.commit()
        return jsonify({'status': 'deleted'})
