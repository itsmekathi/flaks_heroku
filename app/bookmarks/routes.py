from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_login import current_user, login_required
from app import db
from . import bookmarks


@login_required
@bookmarks.route('', methods=["GET", "POST"])
def search():
    return render_template('/bookmarks/_search.bookmarks.html')
