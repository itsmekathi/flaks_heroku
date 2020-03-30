from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_login import current_user, login_required
from app import db
from . import inventory


@login_required
@inventory.route('', methods=["GET", "POST"])
def search():
    return render_template('/inventory/_search.inventory.html')
