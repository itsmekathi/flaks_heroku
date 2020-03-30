from flask import Blueprint
lists = Blueprint('lists', __name__)
from . import routes