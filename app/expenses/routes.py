from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import ExpenseTypeLu, ExpenseCategoryLu, Expenses, ExpenseDetails
from .forms import ExpenseTypeLuForm, ExpenseCategoryLuForm
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
        expense_category = ExpenseTypeLu(
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
