from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  is_admin INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home3.html', username=session['username'])
    else: 
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')     
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username = ? AND password=?", 
            (username, password),
        )  
        user = c.fetchone()

        if user:
            session["username"] = user[1]
            if user[3] == 1:
                    session['is_admin'] = True
            return redirect('/admin')
        else:  
            error = 'Invalid username or password'
            return render_template('signinlogin.html', error=error)
        
    return render_template('signinlogin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect('/login')

@app.route('/admin')
def admin():
    if "is_admin" in session:
        return render_template('signinadmin.html')
    else:
        return redirect('/login')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, 0))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signuplogin.html')
if __name__ == '__main__':
    create_table()
    app.run(debug=True)