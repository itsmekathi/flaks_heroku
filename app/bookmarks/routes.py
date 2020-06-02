from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from app.models import BookmarksFolder, BookmarksItems
from app import db
from . import bookmarks
from .forms import NewBookMarkFolderForm, EditBookMarkFolderForm, DeleteBookMarkFolderForm ,NewBookMarkItemForm, EditBookMarkItemForm, DelteBookMarkItemForm


@login_required
@bookmarks.route('', methods=["GET", "POST"])
def all():
    bookmarks_folders = BookmarksFolder.query.filter_by(
        created_by_id=current_user.id).all()
    bookmarks_items = BookmarksItems.query.filter_by(
        created_by_id=current_user.id).filter_by(folder_id=None).all()
    delete_folder_form = DeleteBookMarkFolderForm()

    return render_template('/bookmarks/all_bookmarks.html', bookmarks_folders=bookmarks_folders, bookmarks_items=bookmarks_items, delete_folder_form = delete_folder_form)


@login_required
@bookmarks.route('/folders/new', methods=["GET", "POST"])
def new_folder():
    form = NewBookMarkFolderForm()
    if form.validate_on_submit():
        bookmark_folder = BookmarksFolder(folder_name=form.folder_name.data,
                                          description=form.description.data,
                                          created_by_id=current_user.id)
        db.session.add(bookmark_folder)
        db.session.commit()
        return redirect(url_for('bookmarks.all'))
    return render_template('/bookmarks/bookmark_folder.html', form=form, legend='New bookmarks folder')


@login_required
@bookmarks.route('/folders/edit/<int:folder_id>', methods=["GET", "POST"])
def edit_folder(folder_id):
    bookmark_folder = BookmarksFolder.query.get_or_404(folder_id)
    form = EditBookMarkFolderForm()
    if form.validate_on_submit():
        bookmark_folder.folder_name = form.folder_name.data
        bookmark_folder.description = form.description.data
        return redirect(url_for('bookmarks.all'))
    form.folder_name.data = bookmark_folder.folder_name
    form.description.data = bookmark_folder.description
    return render_template('/bookmarks/bookmark_folder.html', form=form, legend='Edit Bookmark folder')


@login_required
@bookmarks.route('/folders/<int:folder_id>/delete', methods=["POST"])
def delete_folder(folder_id):
    bookmark_folder = BookmarksFolder.query.get_or_404(folder_id)
    db.session.delete(bookmark_folder)
    db.session.commit()
    try:
        is_ajax = int(request.args["ajax"])
    except:
        is_ajax = 0
    if is_ajax:
        return jsonify({'status': 'Success'})
    else:
        return redirect(url_for('bookmarks.all'))


@login_required
@bookmarks.route('/folders/<int:folder_id>/items/add', methods=["GET", "POST"])
def add_bookmark_item(folder_id):
    form = NewBookMarkItemForm()
    form.folder_id.choices = [(folder.id, folder.folder_name) for folder in BookmarksFolder.query.filter_by(
        created_by_id=current_user.id).all()]
    form.folder_id.choices.insert(0, (0, 'None'))

    if form.validate_on_submit():
        if form.folder_id.data == 0:
            bookmark_item = BookmarksItems(resource_url=form.bookmark_link.data,
                                           description=form.description.data, created_by_id=current_user.id)
        else:
            bookmark_item = BookmarksItems(folder_id=form.folder_id.data, resource_url=form.bookmark_link.data,
                                           description=form.description.data, created_by_id=current_user.id)
        db.session.add(bookmark_item)
        db.session.commit()
        return redirect(url_for('bookmarks.all'))
    form.folder_id.data = folder_id
    return render_template('/bookmarks/bookmark_item.html', form=form, legend='New bookmark item')
