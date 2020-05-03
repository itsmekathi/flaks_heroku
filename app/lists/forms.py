from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField, \
    BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email, InputRequired
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


class ListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(
        min=5, max=100, message="Length of the title should be between 5 to 100 characters")])
    description = TextAreaField('Description', validators=[DataRequired(), InputRequired(), Length(
        min=5, max=100, message="Length of Description should be between 5 to 100 characters")])
    type_id = SelectField('List Type', coerce=int,
                          validators=[DataRequired()])
    sort_order = IntegerField('Sort Order', validators=[DataRequired()])


class NewListForm(ListForm):
    submit = SubmitField('Create')


class EditListForm(ListForm):
    submit = SubmitField('Save')


class DeleteListForm(FlaskForm):
    submit = SubmitField("Delete")


class ListItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=5, max=100, message="Length of the title should be between 5 to 100 characters")])
    description = StringField('Description', validators=[DataRequired(), InputRequired(), Length(
        min=5, max=300, message="Length of Description should be between 5 to 300 characters")])
    sort_order = IntegerField('Sort Order')
    stars = IntegerField('Stars')


class AddListItemForm(ListItemForm):
    submit = SubmitField('Create')


class EditListItemForm(ListItemForm):
    submit = SubmitField("Save")


class DeleteListItemForm(FlaskForm):
    submit = SubmitField("Delete")

class ShowListItemsForm(FlaskForm):
    submit = SubmitField("Show Items")
