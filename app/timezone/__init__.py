from flask import Blueprint
timezone = Blueprint('timezone', __name__)
from . import routes