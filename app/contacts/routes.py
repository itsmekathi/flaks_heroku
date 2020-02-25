from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import ContactTypeLu, Contact, AddressTypeLu, Address
from .forms import ContactTypeLuForm, ContactForm, AddressTypeLuForm, AddressForm
from . import contacts
from datetime import date, datetime


@login_required
@contacts.route('/types', methods=['GET', 'POST'])
def types():
    contact_types = ContactTypeLu.query.all()
    return render_template('/contacts/_contacts.lookups.html', lookups=contact_types, lookup_title='Contact Types')


@login_required
@contacts.route('/types/add', methods=['GET', 'POST'])
def add_types():
    form = ContactTypeLuForm()
    if form.validate_on_submit():
        contact_type = ContactTypeLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(contact_type)
        db.session.commit()
        flash('New contact type has been added ', 'success')
        return redirect(url_for('contacts.types'))
    return render_template('/contacts/_add.contacts.lookups.html', form=form,  legend='Add new contact Type')


@login_required
@contacts.route('/types/edit/<int:type_id>', methods=['GET', 'POST'])
def edit_types(type_id):
    form = ContactTypeLuForm()
    contact_type = ContactTypeLu.query.get_or_404(type_id)
    if form.validate_on_submit():
        contact_type.name = form.name.data
        contact_type.description = form.description.data
        contact_type.icon = form.icon.data
        contact_type.style_class = form.style_class.data
        db.session.add(contact_type)
        db.session.commit()
        flash('Contact type has been Updated ', 'success')
        return redirect(url_for('contacts.types'))
    form.name.data = contact_type.name
    form.description.data = contact_type.description
    form.icon.data = contact_type.icon
    form.style_class.data = contact_type.style_class
    return render_template('/contacts/_add.contacts.lookups.html', form=form, legend='Edit contact Type')


@login_required
@contacts.route('/addresstype', methods=['GET', 'POST'])
def address_types():
    address_types = AddressTypeLu.query.all()
    return render_template('/contacts/_contacts.lookups.html', lookups=address_types, lookup_title="Address Types")


@login_required
@contacts.route('/addresstype/add', methods=['GET', 'POST'])
def add_address_types():
    form = AddressTypeLuForm()
    if form.validate_on_submit():
        address_type = AddressTypeLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(address_type)
        db.session.commit()
        form.name.data = ''
        form.description.data = ''
        form.icon.data = ''
        form.style_class.data = ''
        flash('New address type has been added ', 'success')
        return redirect(url_for('contacts.address_types'))
    return render_template('/contacts/_add.contacts.lookups.html', form=form, legend='Add New Address Type')


@login_required
@contacts.route('/addresstype/edit/<int:type_id>', methods=['GET', 'POST'])
def edit_address_types(type_id):
    form = AddressTypeLuForm()
    address_type = AddressTypeLu.query.get_or_404(type_id)
    if form.validate_on_submit():
        address_type.name = form.name.data
        address_type.description = form.description.data
        address_type.icon = form.icon.data
        address_type.style_class = form.style_class.data
        db.session.add(address_type)
        db.session.commit()
        flash('Address type has been updated ', 'success')
        return redirect(url_for('contacts.address_types'))
    form.name.data = address_type.name
    form.description.data = address_type.description
    form.icon.data = address_type.icon
    form.style_class.data = address_type.style_class
    return render_template('/contacts/_add.contacts.lookups.html', form=form, legend='Edit Address Type')


@login_required
@contacts.route('/new', methods=['GET', 'POST'])
def new_contact():
    form = ContactForm()

    form.contact_type.choices = [(contact_type.id, contact_type.name)
                                 for contact_type in ContactTypeLu.query.order_by('name').all()]
    if form.validate_on_submit():
        contact = Contact(contact_type_id=form.contact_type.data,
                          created_by=current_user, first_name=form.first_name.data,
                          middle_name=form.middle_name.data,
                          last_name=form.last_name.data,
                          image_url=form.image_url.data,
                          email_id=form.email_id.data,
                          phone_number=form.phone_number.data,
                          is_private=form.is_private.data
                          )
        db.session.add(contact)
        db.session.commit()
        form.contact_type.data = ''
        form.first_name.data = ''
        form.middle_name.data = ''
        form.last_name.data = ''
        form.image_url.data = ''
        form.email_id.data = ''
        form.phone_number.data = ''
        form.is_private.data = False
        flash('New contact has been added', 'Success')

    existing_contacts = Contact.query.filter_by(created_by=current_user).all()
    return render_template('/contacts/_contacts.newcontacts.html', form=form, contacts=existing_contacts, title='All contacts', legend='New Contact')


@login_required
@contacts.route('/address/new', methods=['GET', 'POST'])
def new_address():
    form = AddressForm()

    form.address_type.choices = [(address_type.id, address_type.name)
                                 for address_type in AddressTypeLu.query.order_by('name').all()]
    form.contact.choices = [(contact.id, ''.join([contact.first_name, ', ', contact.middle_name,  ' ',  contact.last_name]))
                            for contact in Contact.query.filter_by(created_by=current_user).all()]
    if form.validate_on_submit():
        address = Address(address_type_id=form.address_type.data,
                          contact_id=form.contact.data,
                          created_by=current_user,
                          address_line1=form.address_line1.data,
                          address_line2=form.address_line2.data,
                          address_line3=form.address_line3.data,
                          city=form.city.data,
                          state=form.state.data,
                          country=form.country.data,
                          comments=form.comments.data,
                          latitude=form.latitude.data,
                          longitude=form.longitude.data,
                          is_private=form.is_private.data
                          )
        db.session.add(address)
        db.session.commit()
        form.address_type.data = ''
        form.contact.data = ''
        form.address_line1.data = ''
        form.address_line2.data = ''
        form.address_line3.data = ''
        form.city.data = ''
        form.state.data = ''
        form.country.data = ''
        form.comments.data = ''
        form.latitude.data = ''
        form.longitude.data = ''
        form.is_private.data = False
        flash('New Address has been added', 'Success')

    existing_addresses = Address.query.all()
    return render_template('/contacts/_contacts.newaddress.html', form=form, addresses=existing_addresses, title='All addresses', legend='New Address')
