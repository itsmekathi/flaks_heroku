from flask import Blueprint

personal = Blueprint(__name__)
from . import views