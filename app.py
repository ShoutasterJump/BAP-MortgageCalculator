from flask import Flask, render_template, request
import dbhandler as db
from classes.User import User
import initial.authkey as key
from cryptography.fernet import Fernet

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form["username"]
            result = db.connect("SELECT user_id, username, password FROM users WHERE username = %s", (username,))
            if result:
                db_user_id, db_username, db_password = result[0]
                authkey = key.load_key()
                cipher_suite = Fernet(authkey)
                decrypted_password = cipher_suite.decrypt(bytes(db_password)).decode()
                if request.form["password"] == decrypted_password:
                    user = User(db_user_id, db_username, request.form["password"])
                    return render_template('index.html', user=user)
                else:
                    error = 'Invalid user credentials'
                    return render_template('login.html', error=error)
            else:
                error = 'Invalid user credentials'
                return render_template('login.html', error=error)
        else:
            error = 'An error has occured - please try again'
            return render_template('login.html', error=error)  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        authkey = key.load_key()
        cipher_suite = Fernet(authkey)
        encrypted_password = cipher_suite.encrypt(password.encode())
        result = db.connect("INSERT INTO users (username, password) VALUES (%s, %s)", (username, encrypted_password.decode()))
        if result == True:
            return render_template('login.html', message='Successfully registered')
        else:
            return render_template('register.html', message='Registration failed')
    else:
        error = 'An error has occured - please try again'
        return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    return render_template('login.html')