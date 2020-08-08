from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField, \
    BooleanField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from wtforms.fields.html5 import DateField, TimeField


class BaseJournalForm(FlaskForm):
    tag_line = StringField("How was your day?", validators=[
                           DataRequired(), Length(min=5, max=300)])
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    is_private = BooleanField('Is Private')


class NewJournalForm(BaseJournalForm):
    submit = SubmitField("Submit")


class EditJournalForm(BaseJournalForm):
    submit = SubmitField("Update")
