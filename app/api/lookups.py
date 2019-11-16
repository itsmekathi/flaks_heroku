from . import api
from flask import request, jsonify
from app import db
from app.models import TaskStatusLu, TaskPriorityLu, TaskUrgencyLu


@api.route('/lookups/statuses', methods=["GET"])
def lookup_statuses():
    statuses = TaskStatusLu.query.all()
    return jsonify({'statuses': [status.to_json() for status in statuses]})


@api.route('/lookups/priorities', methods=["GET"])
def lookup_priorities():
    priorities = TaskPriorityLu.query.all()
    return jsonify({'priorities': [priority.to_json() for priority in priorities]})


@api.route('/lookups/urgencies', methods=["GET"])
def lookup_urgencies():
    urgencies = TaskUrgencyLu.query.all()
    return jsonify({'urgencies': [urgency.to_json() for urgency in urgencies]})


@api.route('/lookups', methods=["GET"])
def all_lookups():
    statuses = TaskStatusLu.query.all()
    priorities = TaskPriorityLu.query.all()
    urgencies = TaskUrgencyLu.query.all()
    return jsonify(
        {
            'statuses': [status.to_json() for status in statuses],
            'priorities': [priority.to_json() for priority in priorities],
            'urgencies': [urgency.to_json() for urgency in urgencies]
        })
