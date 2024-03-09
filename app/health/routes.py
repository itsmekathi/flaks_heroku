from . import health
from flask import request, jsonify

from datetime import datetime

@health.route('/', methods=['GET'])
def health_check():
    print('Health OK!')
    return jsonify({"status" : "ok"})