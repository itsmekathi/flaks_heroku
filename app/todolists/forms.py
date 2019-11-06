from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wtforms.fields.html5 import DateField


class ToDoListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description", "rows": "5"})
    submit = SubmitField('Create')


class TaskLuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    style_class = StringField('Style class', validators=[DataRequired()])
    submit = SubmitField('Create')


class ToDoItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(
        max=100)], render_kw={"placeholder": "Title"})
    description = TextAreaField('Description', validators=[DataRequired(), Length(
        max=200)], render_kw={"placeholder": "Description", "rows": "5"})
    status_id = SelectField('Status', coerce=int, validators=[DataRequired()])
    priority_id = SelectField('Priority', coerce=int,
                              validators=[DataRequired()])
    urgency_id = SelectField('Urgency', coerce=int,
                             validators=[DataRequired()])
    scheduled_date = DateField('Scheduled Date', validators=[
                               DataRequired()], format='%Y-%m-%d', render_kw={"placeholder": "MM/dd/YYYY"})
    estimated_duration_hours = IntegerField('Estimated hours', validators=[DataRequired(), NumberRange(
        min=0, max=8, message="Cannot exceed 8 hours")], render_kw={"placeholder": "Hours"})
    estimated_duration_minutes = IntegerField('Estimated minutes', validators=[DataRequired(), NumberRange(
        min=0, max=60, message="Should be b/w 0 to 60")], render_kw={"placeholder": "Minutes"})
    comment = StringField('Comments', validators=[Length(
        max=300)], render_kw={"placeholder": "Comments"})
    submit = SubmitField('Create')


class ToDoItemEditForm(ToDoItemForm):
    submit = SubmitField('Update')


class ActualDurationUpdateForm(ToDoItemForm):
    actual_duration_hours = IntegerField(
        'Actual hours', validators=[DataRequired()])
    actual_duration_minutes = IntegerField(
        'Actual minutes', validators=[DataRequired()])
    submit = SubmitField('Update')

class ToDoItemLogWorkForm(FlaskForm):
    start_datetime = DateTimeField('Start DateTime', validators=[DataRequired()])
    end_datetime= DateTimeField('End Datetime')
    comment = StringField('Comment', validators=[DataRequired("Comment is required"), Length(max=200)])
    submit = SubmitField('Log Work')

