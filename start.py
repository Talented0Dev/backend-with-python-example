from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('forum.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
             username TEXT,
             useremail TEXT,
             password TEXT
        )
    ''')

    conn.commit()
    conn.close()
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        useremail = request.form['useremail']
        # Save the user details to the database
        conn = sqlite3.connect('forum.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, useremail) VALUES (?, ?, ?)", (username, password, useremail))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify user credentials against the database
        conn = sqlite3.connect('forum.db')
        cursor = conn.cursor()

        # Execute a SELECT statement to retrieve the password hash
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchall()

        # Check if the result is not None
        if result is not None:
            for i in range(len(result)):
             # Compare the stored password hash with the user's input using your desired method
             if result[i][0] == password:
                return redirect(url_for('home'))
                break
        else:
            return 'Invalid username or password'

        # Close the database connection
        conn.close()
        
    return render_template('signin.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signout')
def signout():
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run()

