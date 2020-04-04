from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_login import current_user, login_required
from app import db
from app.models import ListTypeLu, ListHeader, ListItem
from . import lists


@login_required
@lists.route('/types', methods=["GET", "POST"])
def list_types():
    lists = ListTypeLu.query.all()
    return render_template('/lists/_all.lists.html', lists=lists)

