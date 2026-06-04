from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
import sqlite3
import time
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session expires after 1 hour

DB_NAME = "database.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    users = cursor.fetchone()
    conn.close()
    return users

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and user[2] == password:
            session['username'] = username
            session['last_active'] = time.time()
            return redirect('/admin')
        else:
            flash('Invalid username or password', 'error')
           
    return render_template('loginsession.html')

@app.route('/admin')
def admin():
    if "username" in session:
        last_active = session.get("last_active")
        if last_active and time.time() - last_active > app.config['PERMANENT_SESSION_LIFETIME']:
            session.clear()
            return redirect("/session_expired")
        session['last_active'] = time.time()
        return render_template('admintime.html', session_timeout=app.config ['PERMANENT_SESSION_LIFETIME'])
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/session_expired')
def session_expired():
    return render_template('session_expired.html')

@app.route('/check_session')        
def check_session():
    if "username" in session:
        return jsonify({"status": "active"})
    else:
        return jsonify({"status": "inactive"})
    
if __name__ == '__main__':
    create_table()
    app.run(debug=True)