from . import api
from flask import request, flash, jsonify
from app import db
from app.models import ContactTypeLu, AddressTypeLu, Address, Contact
from app.api.errors import unauthorized
from flask_login import current_user
from .authentication import auth


@api.route('/contacts/<int:contact_id>', methods=['GET', 'DELETE', 'POST'])
def contacts(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if request.method == "GET":
        return jsonify(contact.to_json())
    if request.method == "DELETE":
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'status': 'deleted'})
    if request.method == "POST":
        # Code to update the entity
        pass
    
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

@api.route('/contacts/addresses/<int:address_id>', methods=['GET', 'DELETE', 'POST'])
def addresses(address_id):
    address = Address.query.get_or_404(address_id)
    if request.method == "GET":
        return jsonify(address.to_json())
    if request.method == "DELETE":
        db.session.delete(address)
        db.session.commit()
        return jsonify({'status': 'deleted'})
    if request.method == "POST":
        # Code to update the entity
        pass
