from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ToDoListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Post')