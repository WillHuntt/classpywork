from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class StudentRegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),Length(min=2, max=50)])
    age = IntegerField('Age', validators=[DataRequired(),NumberRange(min=10, max=99)])
    address = TextAreaField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirm Email', validators=[DataRequired(), Email(), EqualTo('email')])

    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def registration():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        flash(f'Student {form.name.data} registered successfully!', 'Success')
        return redirect(url_for('registration'))
    return render_template('registrationvalidation.html', title='Student Registration', form=form)

if __name__ == '__main__':
    app.run(debug=True)