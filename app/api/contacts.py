from . import api
from flask import request, flash, jsonify
from app import db
from app.models import ContactTypeLu, AddressTypeLu
from app.api.errors import unauthorized
from flask_login import current_user
from .authentication import auth


@api.route('/contacts/types/<int:type_id>', methods=['GET', 'DELETE', 'POST'])
def contacts_types(type_id):
    contact_type = ContactTypeLu.query.get_or_404(type_id)
    if request.method == "GET":
        return jsonify(contact_type.to_json())
    if request.method == "DELETE":
        db.session.delete(contact_type)
        db.session.commit()
        return jsonify({'status': 'deleted'})
    if request.method == "POST":
        # Code to update the entity
        pass


@api.route('/contacts/address_types/<int:type_id>', methods=['GET', 'DELETE', 'POST'])
def address_types(type_id):
    address_type = AddressTypeLu.query.get_or_404(type_id)
    if request.method == "GET":
        return jsonify(address_type.to_json())
    if request.method == "DELETE":
        db.session.delete(address_type)
        db.session.commit()
        return jsonify({'status': 'deleted'})
    if request.method == "POST":
        # Code to update the entity
        pass
