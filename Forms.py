import wtforms
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField
from wtforms.validators import DataRequired, Email
from wtforms import validators, ValidationError
class ContactForm(FlaskForm):
    name = StringField(label='User Name: ', validators=[DataRequired()])
    Gender = RadioField('Gender', choices= [('M', 'Male'),('F', 'Female'), ('O', 'Other')])
    Address = TextAreaField("Address")

    email = TextField("Email", [validators.Required("Please enter your email address"), validators.Email("Please enter your email address in the correct format")])
    Age = IntegerField("age")
    language = SelectField('Languages', choices=[('cpp', 'c++'), ('py', 'python')])
    submit = SubmitField("send")
 