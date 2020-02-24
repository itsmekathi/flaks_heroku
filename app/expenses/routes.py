from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import ExpenseTypeLu, ExpenseCategoryLu, Expenses, ExpenseDetails, Contact, UnitOfMeasurementLu
from .forms import ExpenseTypeLuForm, ExpenseCategoryLuForm, ExpenseForm, ExpenseItemForm, UOMForm
from . import expenses
from datetime import date, datetime


@login_required
@expenses.route('', methods=["GET", "POST"])
def current_expenses():
    # Get the query parameters
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pagesize', 5, type=int)
    user_expenses = Expenses.query.filter_by(created_by=current_user).order_by(Expenses.expense_date_time).paginate(
        page=page, per_page=page_size)
    return render_template('/expenses/_all.expenses.html', expenses=user_expenses)


@login_required
@expenses.route('/add', methods=["GET", "POST"])
def add_expenses():
    expenses_form = ExpenseForm()
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
    expenses_form = ExpenseForm()
    expense_item = ExpenseDetails.query.get_or_404(expense_id)

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
        expense_item.description = expenses_form.description.data, created_on = datetime.utcnow()
        db.session.add(expense_item)
        db.session.commit()
        flash('Expense was successfully updated', 'Success')
        return redirect(url_for('expenses.current_expenses'))
    return render_template('/expenses/_add.expenses.html', form=expenses_form, legend="Edit Expense")


@login_required
@expenses.route('/details/<int:expense_id>', methods=["GET", "POST"])
def details(expense_id):
    expense = Expenses.query.get_or_404(expense_id)
    expense_items = ExpenseDetails.query.filter_by(
        expenses_id=expense_id).all()
    total_expense = sum(
        expense_item.gross_price for expense_item in expense_items)
    return render_template('/expenses/_expense.details.html', expense=expense, expense_items=expense_items, total_expense=total_expense)


@login_required
@expenses.route('/details/add/<int:expense_id>', methods=["GET", "POST"])
def add_details(expense_id):
    expense_item_form = ExpenseItemForm()
    expense_item_form.uom_id.choices = [(uom.id, uom.name)
                                        for uom in UnitOfMeasurementLu.query.all()]
    if expense_item_form.validate_on_submit():
        expense_item = ExpenseDetails(item_name=expense_item_form.item_name.data, expenses_id=expense_id, uom_id=expense_item_form.uom_id.data,
                                      unit_price=expense_item_form.unit_price.data, quantity=expense_item_form.quantity.data,
                                      gross_price=expense_item_form.gross_price.data,created_on=datetime.utcnow(),
                                      modified_on=datetime.utcnow())
        db.session.add(expense_item)
        db.session.commit()
        flash('Expense item was successfully added', 'Success')
        return redirect(url_for('expenses.details', expense_id=expense_item.expenses_id))
    expense_item_form.item_name.data = ''
    expense_item_form.uom_id.data = ''
    expense_item_form.unit_price.data = 0.0
    expense_item_form.quantity.data = 0
    expense_item_form.gross_price.data = 0.0
    expense = Expenses.query.get_or_404(expense_id)
    return render_template('/expenses/_add.expenses.details.html', expense=expense, form=expense_item_form, legend="Add new Item")


@login_required
@expenses.route('/details/edit/<int:expense_detail_id>', methods=["GET", "POST"])
def edit_details(expense_detail_id):
    expense_item = ExpenseDetails.query.get_or_404(expense_detail_id)
    expense_item_form = ExpenseItemForm()
    expense_item_form.uom_id.choices = [(uom.id, uom.name)
                                        for uom in UnitOfMeasurementLu.query.all()]
    if expense_item_form.validate_on_submit():
        expense_item.item_name = expense_item_form.item_name.data
        expense_item.uom_id = expense_item_form.uom_id.data
        expense_item.unit_price = expense_item_form.unit_price.data
        expense_item.quantity = expense_item_form.quantity.data
        expense_item.gross_price = expense_item_form.gross_price.data
        db.session.add(expense_item)
        db.session.commit()
        flash('Expense item was successfully Edited', 'Success')
        return redirect(url_for('expenses.details', expense_id=expense_item.expenses_id))
    expense_item_form.item_name.data = expense_item.item_name
    expense_item_form.uom_id.data = expense_item.uom_id
    expense_item_form.unit_price.data = expense_item.unit_price
    expense_item_form.quantity.data = expense_item.quantity
    expense_item_form.gross_price.data = expense_item.gross_price
    expense = Expenses.query.get_or_404(expense_item.expenses_id)
    return render_template('/expenses/_add.expenses.details.html', expense=expense, form=expense_item_form, legend="Edit Item")


@login_required
@expenses.route('/types', methods=['GET', 'POST'])
def types():
    form = ExpenseTypeLuForm()
    if form.validate_on_submit():
        expense_type = ExpenseTypeLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(expense_type)
        db.session.commit()
        form.name.data = ''
        form.description.data = ''
        form.icon.data = ''
        form.style_class.data = ''
        flash('New expense type has been added ', 'success')
    expense_types = ExpenseTypeLu.query.all()
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_types, legend='Add new expense Type', lookup_titile="Expense Types", offsetUrl='types')


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
        form.icon.data = expense_type.description
        form.style_class.data = expense_type.style_class
    expense_types = ExpenseTypeLu.query.all()
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_types, legend='Edit Expense', lookup_titile="Expense Types", offsetUrl='types')


@login_required
@expenses.route('/categories', methods=['GET', 'POST'])
def categories():
    form = ExpenseCategoryLuForm()
    if form.validate_on_submit():
        expense_category = ExpenseCategoryLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(expense_category)
        db.session.commit()
        form.name.data = ''
        form.description.data = ''
        form.icon.data = ''
        form.style_class.data = ''
        flash('New expense category has been added ', 'success')
    expense_category = ExpenseCategoryLu.query.all()
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_category, legend='Add new expense Category', lookup_titile="Expense Categories", offsetUrl='categories')


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
        form.icon.data = expense_category.description
        form.style_class.data = expense_category.style_class
    expense_categories = ExpenseCategoryLu.query.all()
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_categories, legend='Edit Expense category', lookup_titile="Expense categories", offsetUrl='categories')


@login_required
@expenses.route('/uoms', methods=['GET', 'POST'])
def uoms():
    form = UOMForm()
    if form.validate_on_submit():
        uom = UnitOfMeasurementLu(
            name=form.name.data, description=form.description.data, icon=form.icon.data, style_class=form.style_class.data)
        db.session.add(uom)
        db.session.commit()
        form.name.data = ''
        form.description.data = ''
        form.icon.data = ''
        form.style_class.data = ''
        flash('New UOM has been added ', 'success')
    uoms = UnitOfMeasurementLu.query.all()
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=uoms, legend='Add new UOM', lookup_titile="Unit of measurements", offsetUrl='uoms')


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
        return redirect(url_for('expenses.expense_uoms'))
    if request.method == 'GET':
        form.name.data = expense_uom.name
        form.description.data = expense_uom.description
        form.icon.data = expense_uom.description
        form.style_class.data = expense_uom.style_class
    expense_uoms = UnitOfMeasurementLu.query.all()
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_uoms, legend="Edit UOM", lookup_titile="Unit of measurements", offsetUrl='uoms')
