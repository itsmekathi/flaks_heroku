from flask import render_template, jsonify, url_for, flash, redirect, request, abort, session
from flask_login import current_user, login_required
from app import db
from app.utils import get_first_dateofthemonth
from app.constants import date_time_format
from app.models import ExpenseTypeLu, ExpenseCategoryLu, Expenses, ExpenseDetails, Contact, UnitOfMeasurementLu
from .forms import ExpenseTypeLuForm, ExpenseCategoryLuForm, AddExpenseForm, EditExpenseForm, AddExpenseItemForm, EditExpenseItemForm, UOMForm, ExpenseFilterForm
from . import expenses
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from .constants import from_date_name, to_date_name, selected_category_id_name, selected_contact_id_name, selected_type_id_name


@login_required
@expenses.route('', methods=["GET", "POST"])
def current_expenses():
    # Set the optional query parameters
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pagesize', 5, type=int)

    isPaginationRequest = request.args.get(
        'page', type=int) != None and request.args.get('pagesize', type=int) != None and request.method == 'GET'

    user_expenses_query = Expenses.query.filter_by(created_by=current_user)
    form = ExpenseFilterForm()

    if(isPaginationRequest):
        form.from_date.data = datetime.strptime(
            session.get(from_date_name), date_time_format)
        form.to_date.data = datetime.strptime(
            session.get(to_date_name), date_time_format)
        form.category_id.data = session.get(selected_category_id_name)
        form.type_id.data = session.get(selected_type_id_name)
        form.contact_id.data = session.get(selected_contact_id_name)

    form.contact_id.choices = [(contact.id, contact.first_name)
                               for contact in Contact.query.filter_by(created_by=current_user).all()]
    form.type_id.choices = [
        (type.id, type.name) for type in ExpenseTypeLu.query.all()]
    form.category_id.choices = [
        (category.id, category.name) for category in ExpenseCategoryLu.query.all()]

    form.category_id.choices.insert(0, (0, "All"))
    form.type_id.choices.insert(0, (0, "All"))
    form.contact_id.choices.insert(0, (0, "All"))

    # Init Form fields
    if(form.from_date.data == None):
        form.from_date.data = get_first_dateofthemonth()
    if(form.to_date.data == None):
        form.to_date.data = date.today()
    if(form.category_id.data == None):
        form.category_id.data = 0
    if(form.type_id.data == None):
        form.type_id.data = 0
    if(form.contact_id.data == None):
        form.contact_id.data = 0

    user_expenses_query = user_expenses_query.filter(
        Expenses.expense_date_time >= form.from_date.data)\
        .filter(Expenses.expense_date_time <= (form.to_date.data + timedelta(days=1)))

    if(form.validate_on_submit):
        if form.contact_id.data != None and form.contact_id.data != 0:
            user_expenses_query = user_expenses_query.filter_by(
                expenses_contact_id=form.contact_id.data)
        if form.type_id.data != None and form.type_id.data != 0:
            user_expenses_query = user_expenses_query.filter_by(
                expense_type_id=form.type_id.data)
        if form.category_id.data != None and form.category_id.data != 0:
            user_expenses_query = user_expenses_query.filter_by(
                expense_category_id=form.category_id.data)

        session[from_date_name] = form.from_date.data.strftime(
            date_time_format)
        session[to_date_name] = form.to_date.data.strftime(date_time_format)
        session[selected_contact_id_name] = form.contact_id.data
        session[selected_type_id_name] = form.type_id.data
        session[selected_category_id_name] = form.category_id.data

    total_expense = sum(
        expense.expense_amount for expense in user_expenses_query.all())

    expense_filters = [f'From date: {form.from_date.data.strftime(date_time_format)}',
                       f'To date: {form.to_date.data.strftime(date_time_format)}',
                       f'Type: {form.type_id.data}',
                       f'Category: {form.category_id.data}', f'Contact Id: {form.contact_id.data}',
                       f'Page Number : {page}',
                       f'Page Size: {page_size}']
    user_expenses = user_expenses_query.order_by(Expenses.expense_date_time.desc()).paginate(
        page=page, per_page=page_size)
    return render_template('/expenses/_all.expenses.html', expenses=user_expenses,
                           form=form, legend='Filter Expenses', total_expense=total_expense, expense_filters=expense_filters)


@login_required
@expenses.route('/add', methods=["GET", "POST"])
def add_expenses():
    expenses_form = AddExpenseForm()
    expenses_form.contact_id.choices = [(contact.id, contact.first_name)
                                        for contact in Contact.query.filter_by(created_by=current_user).all()]
    expenses_form.type_id.choices = [
        (type.id, type.name) for type in ExpenseTypeLu.query.all()]
    expenses_form.category_id.choices = [
        (type.id, type.name) for type in ExpenseCategoryLu.query.all()]

    if expenses_form.validate_on_submit():
        expense = Expenses(title=expenses_form.title.data, expense_type_id=expenses_form.type_id.data, expense_category_id=expenses_form.category_id.data,
                           expenses_contact_id=expenses_form.contact_id.data, created_by_id=current_user.id, expense_amount=expenses_form.expense_amount.data,
                           expense_date_time=datetime.combine(
                               date=expenses_form.expense_date.data, time=expenses_form.expense_time.data),
                           description=expenses_form.description.data, created_on=datetime.utcnow())
        db.session.add(expense)
        db.session.commit()
        flash('Expense was successfully added', 'Success')
        return redirect(url_for('expenses.current_expenses'))
    expenses_form.expense_date.data = datetime.now()
    expenses_form.expense_time.data = datetime.now()
    return render_template('/expenses/_add.expenses.html', form=expenses_form, legend="Add New Expense")


@login_required
@expenses.route('/edit/<int:expense_id>', methods=["GET", "POST"])
def edit_expenses(expense_id):
    expenses_form = EditExpenseForm()
    expense_item = Expenses.query.get_or_404(expense_id)

    expenses_form.contact_id.choices = [(contact.id, contact.first_name)
                                        for contact in Contact.query.filter_by(created_by=current_user).all()]
    expenses_form.type_id.choices = [
        (type.id, type.name) for type in ExpenseTypeLu.query.all()]
    expenses_form.category_id.choices = [
        (category.id, category.name) for category in ExpenseCategoryLu.query.all()]

    if expenses_form.validate_on_submit():
        expense_item.title = expenses_form.title.data
        expense_item.expense_type_id = expenses_form.type_id.data
        expense_item.expense_category_id = expenses_form.category_id.data
        expense_item.expenses_contact_id = expenses_form.contact_id.data
        expense_item.created_by_id = current_user.id
        expense_item.expense_amount = expenses_form.expense_amount.data
        expense_item.expense_date_time = datetime.combine(
            date=expenses_form.expense_date.data, time=expenses_form.expense_time.data)
        expense_item.description = expenses_form.description.data
        expense_item.modified_on = datetime.utcnow()
        db.session.add(expense_item)
        db.session.commit()
        flash('Expense was successfully updated', 'Success')
        return redirect(url_for('expenses.current_expenses'))
    expenses_form.title.data = expense_item.title
    expenses_form.type_id.data = expense_item.expense_type_id
    expenses_form.category_id.data = expense_item.expense_category_id
    expenses_form.contact_id.data = expense_item.expenses_contact_id
    expenses_form.expense_amount.data = expense_item.expense_amount
    expenses_form.expense_date.data = expense_item.expense_date_time
    expenses_form.expense_time.data = expense_item.expense_date_time
    expenses_form.description.data = expense_item.description
    return render_template('/expenses/_add.expenses.html', form=expenses_form, legend="Edit Expense")


@login_required
@expenses.route('/<int:expense_id>/details', methods=["GET"])
def details(expense_id):
    expense = Expenses.query.get_or_404(expense_id)
    expense_items = ExpenseDetails.query.filter_by(
        expenses_id=expense_id).all()
    total_expense = sum(
        expense_item.gross_price for expense_item in expense_items)
    expense_item_form = AddExpenseItemForm()
    expense_item_form.uom_id.choices = [(uom.id, uom.name)
                                        for uom in UnitOfMeasurementLu.query.all()]
    details_url = url_for('expenses.get_expenses_details',
                          expense_id=expense_id)
    return render_template('/expenses/_expense.details.html', expense=expense, total_expense=total_expense, form=expense_item_form, legend="Add new item", details_url=details_url)


@login_required
@expenses.route('/<int:expense_id>/details/all', methods=["GET"])
def get_expenses_details(expense_id):
    expense = Expenses.query.filter_by(id=expense_id)\
        .filter_by(created_by_id=current_user.id)
    if expense is None:
        return jsonify({'status': 'No data Found'}), 400
    expense_details = ExpenseDetails.query.filter_by(
        expenses_id=expense_id).all()
    return jsonify({'expenseItems': [expense_item.to_json() for expense_item in expense_details]})


@login_required
@expenses.route('/<int:expense_id>/details/add', methods=["GET", "POST"])
def add_details(expense_id):
    expense_item_form = AddExpenseItemForm()
    expense = Expenses.query.get_or_404(expense_id)
    expense_item_form.uom_id.choices = [(uom.id, uom.name)
                                        for uom in UnitOfMeasurementLu.query.all()]
    if expense_item_form.validate_on_submit():
        expense_item = ExpenseDetails(item_name=expense_item_form.item_name.data, expenses_id=expense_id, uom_id=expense_item_form.uom_id.data,
                                      unit_price=expense_item_form.unit_price.data, quantity=expense_item_form.quantity.data,
                                      gross_price=expense_item_form.gross_price.data, created_on=datetime.utcnow(),
                                      modified_on=datetime.utcnow())
        db.session.add(expense_item)
        db.session.commit()
        update_expense_header(expense_id)
        return jsonify({'status': 'added'})
    if request.method == "GET":
        response_code = 200
    if request.method == "POST":
        response_code = 422
    return render_template('/expenses/_addExpensesDetails.partial.html', form=expense_item_form, legend="Add new item",
                           expense=expense, form_class='add-expense-detail-form', action_name=url_for('expenses.add_details', expense_id=expense_id)), response_code


@login_required
@expenses.route('/<int:expense_id>/details/<int:expense_item_id>', methods=["POST", "GET", "DELETE"])
def detail_item(expense_id, expense_item_id):
    edit_expenses_item_form = EditExpenseItemForm()

    expense = Expenses.query.get_or_404(expense_id)
    expense_item = ExpenseDetails.query.get_or_404(expense_item_id)

    if request.method == "DELETE":
        db.session.delete(expense_item)
        db.session.commit()
        update_expense_header(expense_id)
        return jsonify({'status': 'deleted'})

    edit_expenses_item_form.uom_id.choices = [(uom.id, uom.name)
                                              for uom in UnitOfMeasurementLu.query.all()]

    if edit_expenses_item_form.validate_on_submit():
        expense_item.item_name = edit_expenses_item_form.item_name.data
        expense_item.expenses_id = expense_id
        expense_item.unit_price = edit_expenses_item_form.unit_price.data
        expense_item.quantity = edit_expenses_item_form.quantity.data
        expense_item.gross_price = edit_expenses_item_form.gross_price.data
        expense_item.modified_on = datetime.utcnow()
        db.session.commit()
        update_expense_header(expense_id)
        return jsonify({'status': 'updated'})
    edit_expenses_item_form.item_name.data = expense_item.item_name
    edit_expenses_item_form.unit_price.data = expense_item.unit_price
    edit_expenses_item_form.quantity.data = expense_item.quantity
    edit_expenses_item_form.gross_price.data = expense_item.gross_price
    if request.method == "GET":
        return render_template('/expenses/_addExpensesDetails.partial.html', form=edit_expenses_item_form, legend="Edit item",
                               expense=expense, form_class='edit-expense-item-form',
                               action_name=url_for('expenses.detail_item', expense_id=expense_id, expense_item_id=expense_item.id))
    else:
        return render_template('/expenses/_addExpensesDetails.partial.html', form=edit_expenses_item_form, legend="Edit item",
                               expense=expense, form_class='edit-expense-item-form',
                               action_name=url_for('expenses.detail_item', expense_id=expense_id, expense_item_id=expense_item.id)), 422


def update_expense_header(expense_id):
    expense = Expenses.query.get_or_404(expense_id)
    expense_items = ExpenseDetails.query.filter_by(
        expenses_id=expense_id).all()
    total_expense = sum(
        expense_item.gross_price for expense_item in expense_items)
    expense.expense_amount = total_expense
    db.session.add(expense)
    db.session.commit()
    return


@login_required
@expenses.route('/types', methods=['GET', 'POST'])
def types():
    expense_types = [construct_type_with_editLink(
        expense_type) for expense_type in ExpenseTypeLu.query.all()]
    return render_template('/expenses/_expenses.lookups.html', lookups=expense_types, lookup_titile="Expense Types", offsetUrl='types')


def construct_type_with_editLink(expense_type):
    expense_type.edit_link = url_for(
        'expenses.edit_types', type_id=expense_type.id)
    return expense_type


@login_required
@expenses.route('/types/add', methods=['GET', 'POST'])
def add_types():
    form = ExpenseTypeLuForm()
    if form.validate_on_submit():
        expense_type = ExpenseTypeLu(name=form.name.data, description=form.description.data,
                                     icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(expense_type)
        db.session.commit()
        flash('The expense type has been Added', 'success')
        return redirect(url_for('expenses.types'))
    return render_template('/expenses/_add.expenses.lookups.html', form=form, legend='Add Expense Types')


@login_required
@expenses.route('/types/edit/<int:type_id>', methods=['GET', 'POST'])
def edit_types(type_id):
    form = ExpenseTypeLuForm()
    expense_type = ExpenseTypeLu.query.get_or_404(type_id)
    if form.validate_on_submit():
        expense_type.name = form.name.data
        expense_type.description = form.description.data
        expense_type.icon = form.icon.data
        expense_type.style_class = form.style_class.data
        db.session.add(expense_type)
        db.session.commit()
        flash('The expense type has been updated', 'success')
        return redirect(url_for('expenses.types'))
    if request.method == 'GET':
        form.name.data = expense_type.name
        form.description.data = expense_type.description
        form.icon.data = expense_type.icon
        form.style_class.data = expense_type.style_class
    expense_types = ExpenseTypeLu.query.all()
    return render_template('/expenses/_add.expenses.lookups.html', form=form, legend='Edit Expense Types')


@login_required
@expenses.route('/categories', methods=['GET', 'POST'])
def categories():
    expense_category = [construct_category_with_editLink(
        category) for category in ExpenseCategoryLu.query.all()]
    return render_template('/expenses/_expenses.lookups.html',  lookups=expense_category,  lookup_titile="Expense Categories", offsetUrl='categories')


def construct_category_with_editLink(category):
    category.edit_link = url_for(
        'expenses.edit_categories', category_id=category.id)
    return category


@login_required
@expenses.route('/categories/add', methods=['GET', 'POST'])
def add_categories():
    form = ExpenseCategoryLuForm()
    if form.validate_on_submit():
        expense_category = ExpenseCategoryLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(expense_category)
        db.session.commit()
        flash('New expense category has been Added', 'success')
        return redirect(url_for('expenses.categories'))
    return render_template('/expenses/_add.expenses.lookups.html', form=form, legend='Add Expense Category')


@login_required
@expenses.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_categories(category_id):
    form = ExpenseCategoryLuForm()
    expense_category = ExpenseCategoryLu.query.get_or_404(category_id)
    if form.validate_on_submit():
        expense_category.name = form.name.data
        expense_category.description = form.description.data
        expense_category.icon = form.icon.data
        expense_category.style_class = form.style_class.data
        db.session.add(expense_category)
        db.session.commit()
        flash('The expense category has been updated', 'success')
        return redirect(url_for('expenses.categories'))
    if request.method == 'GET':
        form.name.data = expense_category.name
        form.description.data = expense_category.description
        form.icon.data = expense_category.icon
        form.style_class.data = expense_category.style_class
    return render_template('/expenses/_add.expenses.lookups.html', form=form, legend='Edit Expense category')


@login_required
@expenses.route('/uoms', methods=['GET', 'POST'])
def uoms():
    uoms = [construct_uom_witheditlink(uom)
            for uom in UnitOfMeasurementLu.query.all()]
    return render_template('/expenses/_expenses.lookups.html',  lookups=uoms,  lookup_titile="Unit of measurements", offsetUrl='uoms')


def construct_uom_witheditlink(uom):
    uom.edit_link = url_for('expenses.edit_uoms', uom_id=uom.id)
    return uom


@login_required
@expenses.route('/uom/add', methods=['GET', 'POST'])
def add_uoms():
    form = UOMForm()
    if form.validate_on_submit():
        expense_uom = UnitOfMeasurementLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(expense_uom)
        db.session.commit()
        flash('The expense UOM has been added', 'success')
        return redirect(url_for('expenses.uoms'))
    return render_template('/expenses/_add.expenses.lookups.html', form=form, legend="Add UOM")


@login_required
@expenses.route('/uom/edit/<int:uom_id>', methods=['GET', 'POST'])
def edit_uoms(uom_id):
    form = UOMForm()
    expense_uom = UnitOfMeasurementLu.query.get_or_404(uom_id)
    if form.validate_on_submit():
        expense_uom.name = form.name.data
        expense_uom.description = form.description.data
        expense_uom.icon = form.icon.data
        expense_uom.style_class = form.style_class.data
        db.session.add(expense_uom)
        db.session.commit()
        flash('The expense UOM has been updated', 'success')
        return redirect(url_for('expenses.uoms'))
    if request.method == 'GET':
        form.name.data = expense_uom.name
        form.description.data = expense_uom.description
        form.icon.data = expense_uom.icon
        form.style_class.data = expense_uom.style_class
    expense_uoms = UnitOfMeasurementLu.query.all()
    return render_template('/expenses/_add.expenses.lookups.html', form=form, legend="Edit UOM")
