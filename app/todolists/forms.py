from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ToDoListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators = [DataRequired()])
    submit = SubmitField('Create')
class TaskLuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    style_class = StringField('Style class', validators=[DataRequired()])
    submit = SubmitField('Create')

# class ToDoItemForm(FlaskForm):
#     title = StringField('Title', validators = [DataRequired()] )
#     description = TextAreaField('Description', validators = [DataRequired])
