from flask import Flask, render_template, request, flash, redirect, url_for
app = Flask(__name__)
app.secret_key = 'random string'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods = ['POST, GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username']!='admin' or request.form['password']!='admin':
            error = 'Invalid username or password.'
            print("error messages")
        else: 
            flash('You were successfully logged in')
            flash('Log out before login again')
            return redirect(url_for('index'))
        return render_template('log_in.html', error=error)

if __name__=='__main__':
    app.run(debug=True)
