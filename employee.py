# Import the Flask framework and functions needed for rendering pages
# and handling form data submitted by the user
from flask import Flask, render_template, request

# Import Flask-WTF so we can create forms more easily
from flask_wtf import FlaskForm

# Import different field types for our forms
from wtforms import StringField, IntegerField, FloatField, validators

# Import a validator that checks if input was provided
from wtforms.validators import InputRequired


# Create the Flask application
app = Flask(__name__)

# Secret key is required for Flask-WTF forms
# It helps protect against CSRF attacks
app.config['SECRET_KEY'] = 'your_secret'


# ------------------------------
# Employee Information Form
# ------------------------------
# This form stores basic employee details
class EmployeeInfo(FlaskForm):

    # Text field for the employee's full name
    # InputRequired() makes sure the field is not left empty
    fullName = StringField(
        'Full Name',
        [validators.InputRequired()]
    )

    # Text field for the employee's department
    dept = StringField(
        'Department',
        [validators.InputRequired()]
    )


# ------------------------------
# Company Details Form
# ------------------------------
# This form stores additional employee/company-related info
class CompanyDetails(FlaskForm):

    # Integer field for years of experience
    # Only whole numbers can be entered
    yearsofExp = IntegerField(
        'Years of Experience',
        [validators.InputRequired()]
    )


# ------------------------------
# Custom Function
# ------------------------------
# This function takes a value and prints out
# a message showing the employee's experience
def custom_function(val):

    print(f"This employee has {val} years of experience.")