from flask import Blueprint
todolists = Blueprint('todolists', __name__)
from . import routes
