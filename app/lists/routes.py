from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import ListTypeLu, ListHeader, ListItem
from . import lists
from .forms import NewListForm, AddListItemForm
from datetime import datetime


@login_required
@lists.route('')
def all_lists():
    """ Render all lists as accordian with items
    should be expandable and collapsable
    """
    items = ListHeader.query.all()
    return render_template('/lists/all_lists.html', items=items)


@login_required
@lists.route('/new', methods=["GET", "POST"])
def new_lists():
    """Create new list, you would have to choose a list type
       and title and visiblity
    """
    form = NewListForm()
    form.type_id.choices = [(list_type.id, list_type.name)
                            for list_type in ListTypeLu.query.all()]
    if form.validate_on_submit():
        new_list = ListHeader(name=form.title.data, description=form.description.data,
                              type_id=form.type_id.data, sort_order=form.sort_order.data,
                              created_by_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('lists.all_lists'))

    return render_template('/lists/new.lists.html', form=form, legend="Add New List")


@login_required
@lists.route('/<int:list_id>/delete')
def delete_list(list_id):
    """ Delete the list and its associated items
    """
    list_items = ListItem.query.filter_by(list_id=list_id).all()
    db.session.remove(list_items)
    db.session.commit()
    list_header = ListHeader.query.filter_by(id=list_id).all()
    db.session.remove(list_header)
    db.session.commit()
    return redirect(url_for('lists.all_lists'))


@login_required
@lists.route('/<int:list_id>/details')
def list_details(list_id):
    """ Page which returns the list items provided
        the list id
    """
    list_header = ListHeader.query.get_or_404(list_id)
    list_items = ListItem.query.filter_by(list_id=list_id).all()
    try:
        is_ajax = int(request.args["ajax"])
    except:
        is_ajax = 0
    if is_ajax:
        response = list_header.to_json()
        response['listItems'] = [list_item.to_json()
                                 for list_item in list_items]
        return jsonify(listData=response)
    return render_template('/lists/list_details.html', list_header=list_header)


@login_required
@lists.route('/<int:list_id>/add', methods=["GET", "POST"])
def add_list_item(list_id):
    """ Page where user can add items to list
    """
    form = AddListItemForm(request.args)
    if form.validate_on_submit():
        list_item = ListItem(
            list_id=list_id, 
            name=form.name.data, 
            description=form.description.data, 
            sort_order=form.sort_order.data, 
            stars=form.stars.data,
            created_on=datetime.utcnow())
        db.session.add(list_item)
        db.session.commit()
        return redirect(url_for('lists.list_details', list_id=list_id))
    return render_template('/lists/add_list_items.html', form=form)


@login_required
@lists.route('/types', methods=["GET", "POST"])
def list_types():
    list_types = ListTypeLu.query.all()
    return render_template('/lists/list_types.html', list_types=list_types)
