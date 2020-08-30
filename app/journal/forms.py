from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from flask_pagedown.fields import PageDownField


class BaseJournalForm(FlaskForm):
    tag_line = StringField("How was your day?", validators=[
                           DataRequired(), Length(min=5, max=300)])
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    is_private = BooleanField('Is Private')

class NewJournalForm(BaseJournalForm):
    submit = SubmitField("Submit")

class EditJournalForm(BaseJournalForm):
    submit = SubmitField("Update")
