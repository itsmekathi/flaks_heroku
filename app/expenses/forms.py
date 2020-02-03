from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField, \
    BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from wtforms.fields.html5 import DateTimeField


class ExpenseTypeLuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=1, max=100, message="Maximum length for name is 100 characters")])
    description = TextAreaField('Description', validators=[DataRequired(
    ), Length(min=1, max=300, message="Maximum length for description is 300 characters.")], render_kw={"placeholder": "Description", "rows": "5"})
    icon = StringField('Icon', validators=[DataRequired(), Length(
        min=1, max=100, message='Icon length exceeds the specified lenght of 100')])
    style_class = StringField('Style Class', validators=[DataRequired(), Length(
        min=1, max=100, message='Style class length exceeds the specified lenght of 100')])
    submit = SubmitField('Create')


class ExpenseCategoryLuForm(ExpenseTypeLuForm):
    pass


class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100, message="Maximum length for title is 100 characters")])
    contact_id=SelectField('Expense Contact', coerce=int,
                           validators=[DataRequired()])
    type_id=SelectField('Expense Type', coerce=int,
                        validators=[DataRequired()])
    category_id=SelectField('Expense Category', coerce=int,
                              validators=[DataRequired()])
    expense_amount=DecimalField(
        'Expense amount', places=2, validators=[DataRequired()])
    expense_date_time=DateTimeField(
        'Expense Date time', validators=[DataRequired()], render_kw={"placeholder": "MM/dd/YYYY HH:MM:SS"})
    description = TextAreaField('Description', validators=[DataRequired(), Length(
        max=300)], render_kw={"placeholder": "Description", "rows": "5"})
    submit = SubmitField('Create')
    
