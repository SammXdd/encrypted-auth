from flask import Flask, request, render_template, redirect, url_for, flash, session
import json
import os
from enc import encode_password

app = Flask(__name__)
app.secret_key = 'heywassupp' 

USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as file:
        json.dump(users, file)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        if username in users:
            flash("Username already taken. Please choose a different username.")
            return redirect(url_for('register'))
        
        # encrypt password and save it to json
        encoded_password = encode_password(password)
        users[username] = encoded_password
        save_users(users)
        flash("User registered successfully! Please log in.")
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        encoded_password = encode_password(password)
        stored_password = users.get(username)
        
        if stored_password == encoded_password:
            session['username'] = username  # session management
            flash("Logged in successfully!")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None) 
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)
