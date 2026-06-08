from flask import Flask, request, redirect
from flask.templating import render_template
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"Name: {self.first_name}, {self.last_name}, age: {self.age}"
    
@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('indexsql1.html', profiles=profiles)

@app.route('/add_data')
def add_data():
    return render_template('add_profile1.html')
   
@app.route('/add', methods=['POST'])
def profile():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')

    if first_name !='' and last_name !='' and age is not None:
        p = Profile(first_name=first_name, last_name=last_name, age=age)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)