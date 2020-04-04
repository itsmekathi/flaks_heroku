from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField, \
    BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from wtforms.fields.html5 import DateField, TimeField


class ListTypeLuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=1, max=100, message="Maximum length for name is 100 characters")])
    description = TextAreaField('Description', validators=[DataRequired(
    ), Length(min=1, max=300, message="Maximum length for description is 300 characters.")], render_kw={"placeholder": "Description", "rows": "3"})
    icon = StringField('Icon', validators=[DataRequired(), Length(
        min=1, max=100, message='Icon length exceeds the specified lenght of 100')])
    style_class = StringField('Style Class', validators=[DataRequired(), Length(
        min=1, max=100, message='Style class length exceeds the specified lenght of 100')])
    sort_order = IntegerField('Expense amount', validators=[DataRequired()])
    submit = SubmitField('Create')
