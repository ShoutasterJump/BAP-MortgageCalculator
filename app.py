from flask import Flask, render_template, request, session, redirect, url_for
import dbhandler as db
from classes.User import User
import initial.authkey as key
from cryptography.fernet import Fernet
from classes.Mortgage import Mortgage
from analysis import *
from graphing import *

app = Flask(__name__)
app.secret_key = '1cef852fb2a2a4f81a71deeb3b7ab273818b62500685bb72feb0965dc0004cc9'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        result = db.connect("SELECT user_id, username, password FROM users WHERE username = %s", (username,))
        if result:
            db_user_id, db_username, db_password = result[0]
            authkey = key.load_key()
            cipher_suite = Fernet(authkey)
            decrypted_password = cipher_suite.decrypt(bytes(db_password)).decode()
            if request.form["password"] == decrypted_password:
                user = User(db_user_id, db_username, request.form["password"])
                session['username'] = user.username
                session['user_id'] = user.userID
                return redirect(url_for('home'))
            else:
                error = 'Invalid user credentials'
        else:
            error = 'Invalid user credentials'
    return render_template('login.html', error=error) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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
    return render_template('register.html')
    
@app.route('/home', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')
    
@app.route('/new_mortgage', methods=['GET','POST'])
def new_mortgage():
    error = ""
    mortgage_data = {
        "mortgage_name": "Add mortgage name",
        "principal": "Amount",
        "interest_rate": "% p.a",
        "deposit": "Amount",
        "start_date": "start-date",
        "extra_costs": "Amount",
        "term": "Years"
    }
    analysis_summary = None
    graph_div = None
    if request.method == 'POST':
        try:
            user_id = session.get('user_id')
            mortgage_data = {
                "mortgage_name": request.form["mortgage-name"],
                "principal": request.form["principal"],
                "interest_rate": request.form["interest-rate"],
                "deposit": request.form["deposit"],
                "start_date": request.form["start-date"],
                "extra_costs": request.form["extra-costs"],
                "term": request.form["term"]
            }
            
            
            mortgage = Mortgage(
                request.form["mortgage-name"],
                request.form["start-date"],
                request.form["interest-rate"],
                request.form["term"],
                request.form["principal"],
                request.form["extra-costs"],
                request.form["deposit"]
            )
            
            analysis_summary = newMortgageSummary(mortgage)
            graph_div = newMortgageGraph(mortgage)
            # test = db.connect("INSERT INTO mortgages (user_id, mortgage_name, estab_date, initial_interest, initial_term, initial_principal, extra_cost, deposit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       # (user_id, mortgage.mortgageName, mortgage.estabDate, mortgage.initialInterest, mortgage.initialTerm, mortgage._initialPrincipal, mortgage.extraCost, mortgage.desposit))
        except Exception as e:
            return render_template('new_mortgage.html', error=str(e))
    return render_template('new_mortgage.html', error=error, mortgage_data=mortgage_data, analysis_result=analysis_summary, graph_div=graph_div)
    
@app.route('/update_mortgage', methods=['GET','POST'])
def update_mortgage():
    if request.method == 'GET':
        return render_template('update_mortgage.html')
    elif request.method == 'POST':
        pass

@app.route('/remove_data', methods=['GET','POST'])
def remove_data():
    if request.method == 'GET':
        return render_template('remove_data.html')
    elif request.method == 'POST':
        pass
    
@app.route('/user_settings', methods=['GET','POST'])
def user_settings():
    if request.method == 'GET':
        return render_template('user_settings.html')
    elif request.method == 'POST':
        pass

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)