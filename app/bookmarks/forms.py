from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField, \
    BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email, InputRequired, URL
from wtforms.fields import DateField, TimeField

class BookMarkFolderForm(FlaskForm):
    folder_name = StringField('Folder Name', validators=[DataRequired(), Length(
        min=5, max=100, message="Length of the title should be between 5 to 100 characters")])
    description = TextAreaField('Description', validators=[DataRequired(), InputRequired(), Length(
        min=5, max=100, message="Length of Description should be between 5 to 300 characters")])


class NewBookMarkFolderForm(BookMarkFolderForm):
    submit = SubmitField('Create')

class EditBookMarkFolderForm(BookMarkFolderForm):
    submit = SubmitField('Update')

class DeleteBookMarkFolderForm(FlaskForm):
    submit = SubmitField("Delete")

class BookMarkItemForm(FlaskForm):
    folder_id = SelectField('Choose Folder', coerce=int,
                          validators=[DataRequired()])
    bookmark_link = StringField('Link', validators=[DataRequired(), InputRequired(), URL(require_tld=True)])
    description = TextAreaField('Description', validators=[DataRequired(), InputRequired(), Length(
        min=5, max=100, message="Length of Description should be between 5 to 300 characters")])

class NewBookMarkItemForm(BookMarkItemForm):
    submit = SubmitField("Create")

class EditBookMarkItemForm(BookMarkItemForm):
    submit = SubmitField("Update")

class DelteBookMarkItemForm(FlaskForm):
    submit= SubmitField("Delete")
    

                    