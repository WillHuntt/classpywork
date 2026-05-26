from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Enrollment.db"
app.config['SECRET_KEY'] = 'random string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class student(db.Model):
    idNumber = db.Column('StdID',db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Address = db.Column(db.String(200))
    City = db.Column(db.String(50))

    def __init__(self, FirstName,LastName,Address,City):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Address = Address
        self.City = City

@app.route('/')
def show_all():
    return render_template('show_all.html', student=student.query.all())

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method=='POST':
        if not request.form['FirstName'] or not request.form['LastName'] or \
        not request.form['Address'] or not request.form['City']:
            flash('Please enter all the fields', 'error')
        else:
            studentmain = student(request.form['FirstName'],
                                  request.form['LastName'],
                                  request.form['Address'],
                                  request.form['City'])
            db.session.add(studentmain)
            db.session.commit()

            flash("Record inserted!")
            return redirect(url_for('show_all'))
        
    return render_template('new.html')
    
if(__name__=="__main__"):

    app.run(debug=True)