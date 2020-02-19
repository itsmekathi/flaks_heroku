from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import ExpenseTypeLu, ExpenseCategoryLu, Expenses, ExpenseDetails, Contact, UnitOfMeasurementLu
from .forms import ExpenseTypeLuForm, ExpenseCategoryLuForm, ExpenseForm, ExpenseItemForm, UOMForm
from . import expenses
from datetime import date, datetime


@login_required
@expenses.route('/types', methods=['GET', 'POST'])
def expense_types():
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
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_types, legend='Add new expense Type', lookup_titile="Expense Types")


@login_required
@expenses.route('/categories', methods=['GET', 'POST'])
def expense_categories():
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
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=expense_category, legend='Add new expense Category', lookup_titile="Expense Categories")


@login_required
@expenses.route('/uoms', methods=['GET', 'POST'])
def expense_uoms():
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
    return render_template('/expenses/_expenses.lookups.html', form=form, lookups=uoms, legend='Add new UOM', lookup_titile="Unit of measurements")


@login_required
@expenses.route('', methods=["GET", "POST"])
def current_expenses():
    # Get the query parameters
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pagesize', 5, type=int)

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
                           expense_date_time=expenses_form.expense_date_time.data, description=expenses_form.description.data, created_on=datetime.utcnow())
        db.session.add(expense)
        db.session.commit()
        flash('Expense was successfully added', 'Success')
        expenses_form.title.data = ''
        expenses_form.contact_id.data = ''
        expenses_form.type_id.data = ''
        expenses_form.category_id.data = ''
        expenses_form.expense_amount.data = 0.0
        expenses_form.description.data = ''
    expenses_form.expense_date_time.data = datetime.now()

    user_expenses = Expenses.query.filter_by(created_by=current_user).order_by(Expenses.expense_date_time).paginate(
        page=page, per_page=page_size)
    return render_template('/expenses/_all.expenses.html', expenses=user_expenses, form=expenses_form, legend="Add New Expense")


@login_required
@expenses.route('/details/<int:expense_id>', methods=["GET", "POST"])
def details(expense_id):
    expense_item_form = ExpenseItemForm()
    expense_item_form.uom_id.choices = [(uom.id, uom.name)
                                        for uom in UnitOfMeasurementLu.query.all()]
    if expense_item_form.validate_on_submit():
        expense_item = ExpenseDetails(item_name=expense_item_form.item_name.data, expenses_id=expense_id, uom_id=expense_item_form.uom_id.data,
                                      unit_price=expense_item_form.unit_price.data, quantity=expense_item_form.quantity.data, gross_price=expense_item_form.gross_price.data)
        db.session.add(expense_item)
        db.session.commit()
        flash('Expense item was successfully added', 'Success')
        expense_item_form.item_name.data = ''
        expense_item_form.uom_id.data = ''
        expense_item_form.unit_price.data = ''
        expense_item_form.quantity.data = ''
        expense_item_form.gross_price.data = ''
    expense = Expenses.query.get_or_404(expense_id)
    expense_items = ExpenseDetails.query.filter_by(
        expenses_id=expense_id).all()
    total_expense = sum(
        expense_item.gross_price for expense_item in expense_items)
    return render_template('/expenses/_expense.details.html', expense=expense, expense_items=expense_items, form=expense_item_form, legend="Add new Item", total_expense=total_expense)
