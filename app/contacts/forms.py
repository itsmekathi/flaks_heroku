from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from wtforms.fields import DateField


class ContactTypeLuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=1, max=100, message="Maximum length for name is 100 characters")])
    description = TextAreaField('Description', validators=[DataRequired(
    ), Length(min=1, max=300, message="Maximum length for description is 300 characters.")], render_kw={"placeholder": "Description", "rows": "5"})
    icon = StringField('Icon', validators=[DataRequired(), Length(
        min=1, max=100, message='Icon length exceeds the specified lenght of 100')])
    style_class = StringField('Style Class', validators=[DataRequired(), Length(
        min=1, max=100, message='Style class length exceeds the specified lenght of 100')])
    submit = SubmitField('Create')


class AddressTypeLuForm(ContactTypeLuForm):
    pass


class ContactForm(FlaskForm):
    contact_type = SelectField(
        'Contact Type', coerce=int, validators=[DataRequired()])
    first_name = StringField('First Name', validators=[
                             DataRequired(), Length(min=1, max=100)])
    middle_name = StringField('Middle Name', validators=[
                              DataRequired(), Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[
                            DataRequired(), Length(min=1, max=100)])
    image_url = StringField('Image URL', validators=[Length(0, 200)])
    email_id = StringField('Email Id', validators=[
                           Email(), Length(min=0, max=200)])
    phone_number = StringField('Phone Number')
    is_private = BooleanField('Is Private')
    submit = SubmitField('Create')


class AddressForm(FlaskForm):
    address_type = SelectField(
        'Address Type', coerce=int, validators=[DataRequired()])
    contact = SelectField('Contact', coerce=int, validators=[DataRequired()])
    address_line1 = StringField('Address Line 1', validators=[
        DataRequired(), Length(min=1, max=200)])
    address_line2 = StringField('Address Line 2', validators=[
        DataRequired(), Length(min=1, max=200)])
    address_line3 = StringField('Address Line 3', validators=[
        DataRequired(), Length(min=1, max=200)])
    city = StringField('City', validators=[
        DataRequired(), Length(min=1, max=200)])
    state = StringField('State', validators=[
        DataRequired(), Length(min=1, max=200)])
    country = StringField('Country', validators=[
        DataRequired(), Length(min=1, max=200)])
    comments = StringField('Comments', validators=[
        DataRequired(), Length(min=1, max=300)])
    latitude = StringField('Latitude', validators=[
        DataRequired(), Length(min=1, max=100)])
    longitude = StringField('Longitude', validators=[
                            DataRequired(), Length(min=1, max=100)])
    is_private = BooleanField('Is Private')
    submit = SubmitField('Create')
