from flask import Blueprint
contacts = Blueprint('contacts', __name__)
from . import routes
