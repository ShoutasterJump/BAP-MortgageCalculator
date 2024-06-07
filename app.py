from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import dbhandler as db
from classes.User import User
import initial.authkey as key
from cryptography.fernet import Fernet
from classes.Mortgage import Mortgage
from amortization import *
from analysis import *
from graphing import *
from classes.Transaction import Transaction
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

def fetch_mortgage_data(mortgage_id):
    if not mortgage:
        print("No mortgage information available")
        return {}
    
    mortgages = []
    transactions= []
    if len(mortgage_id) == 1:
        mortgage = db.connect("SELECT * FROM mortgages WHERE mortgage_id = %s", (mortgage_id,))
        print(mortgage)
        mortgage = mortgage[0]
        mortgage_instance = Mortgage(
            mortgage[2],  # mortgage_name
            mortgage[3],  # estab_date
            float(mortgage[4]),  # initial_interest
            int(mortgage[5]),  # initial_term
            float(mortgage[6]),  # initial_principal
            float(mortgage[7]),  # extra_cost
            float(mortgage[8])  # deposit
        )
        mortgages.append(mortgage_instance)
        
        transaction_instances = db.connect("SELECT * FROM transactions WHERE mortgage_id = %s", (mortgage_id,))
        for trans in transaction_instances:
            transaction_instance = Transaction(
                float(trans[2]),  # current_principal
                float(trans[3]),  # current_interest
                trans[4],  # start_date
                int(trans[5]),  # remaining_years
                int(trans[6]),  # remaining_months
                float(trans[7]),  # extra_payment
                trans[8],  # extra_payment_type
                float(trans[9]),  # balloon_payment
                trans[10]  # comment
            )
            transactions.append(transaction_instance)
    else:
        for i in mortgage_id:
            mortgage = mortgage = db.connect("SELECT * FROM mortgages WHERE mortgage_id = %s", (i,))
            print(mortgage)
            mortgage = mortgage[0]
            mortgage_instance = Mortgage(
                mortgage[2],  # mortgage_name
                mortgage[3],  # estab_date
                float(mortgage[4]),  # initial_interest
                int(mortgage[5]),  # initial_term
                float(mortgage[6]),  # initial_principal
                float(mortgage[7]),  # extra_cost
                float(mortgage[8])  # deposit
            )
            mortgages.append(mortgage_instance)
            
            transaction_instances = db.connect("SELECT * FROM transactions WHERE mortgage_id = %s", (i,))
            for trans in transaction_instances:
                transaction_instance = Transaction(
                    float(trans[2]),  # current_principal
                    float(trans[3]),  # current_interest
                    trans[4],  # start_date
                    int(trans[5]),  # remaining_years
                    int(trans[6]),  # remaining_months
                    float(trans[7]),  # extra_payment
                    trans[8],  # extra_payment_type
                    float(trans[9]),  # balloon_payment
                    trans[10]  # comment
                )
                transactions.append(transaction_instance)
    
    # Perform analysis
    analysis_summary = mortgage_analysis(mortgages, transactions, "detailed_summary", datetime.now())
    graph_json = mortgage_graph(mortgages, transactions, "Monthly")
    graph_div = json.loads(graph_json)
    amortization_table_html = generate_amortization_table_html(
        mortgage_analysis(mortgages, transactions, "amortization", datetime.now())["monthly_amortization"]
    )
    
    result = {
        "estimated_repayments": analysis_summary.get('estimated_repayments', 0),
        "full_term_to_amortize": analysis_summary.get('full_term_to_amortize', 0),
        "interest": analysis_summary.get('interest', 0),
        "estimated_reduced_term_to_amortize": analysis_summary.get('estimated_reduced_term_to_amortize', 0),
        "principal": analysis_summary.get('principal', 0),
        "interest_over_term": analysis_summary.get('interest_over_term', 0),
        "extra": analysis_summary.get('extra', 0),
        "total_principal_interest": analysis_summary.get('total_principal_interest', 0),
        "repayment": analysis_summary.get('repayment', 0),
        "interest_over_reduced_term": analysis_summary.get('interest_over_reduced_term', 0),
        "payments_over_term": analysis_summary.get('payments_over_term', 0),
        "interest_saved_over_reduced_term": analysis_summary.get('interest_saved_over_reduced_term', 0),
        "payments_over_reduced_term": analysis_summary.get('payments_over_reduced_term', 0),
        "total_principal_interest_over_reduced_term": analysis_summary.get('total_principal_interest_over_reduced_term', 0),
        "graph_data": graph_div,
        "amortization_table": amortization_table_html
    }
    
    print(f"fetch_mortgage_data result: {result}")
    print(f"Result type: {type(result)}")

    return result

@app.route('/home', methods=['GET','POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get("user_id")
    mortgages = db.connect("SELECT * FROM mortgages WHERE user_id = %s", (user_id,))
    
    if isinstance(mortgages, list):
        mortgage_buttons = [{'id': mortgage[0], 'name': mortgage[2]} for mortgage in mortgages]
    else:
        mortgage_buttons= []
        
    # Determine default selection
    if len(mortgage_buttons) > 1:
        default_selection = 'Combined'
    elif len(mortgage_buttons) == 1:
        default_selection = mortgage_buttons[0]['name']
    else:
        default_selection = None
        
    if default_selection == 'Combined':
        mortgage_query = [mortgage_buttons[mortgage]['id'] for mortgage in mortgage_buttons]
        initial_data = fetch_mortgage_data(mortgage_query)
    elif default_selection:
        initial_data = fetch_mortgage_data(mortgage_buttons[0]['id'])
    else:
        initial_data = None
    
    return render_template('index.html', mortgages=mortgage_buttons, default_selection=default_selection, initial_data=initial_data)

@app.route('/get_data/<string:option>', methods=['GET'])
def get_data(option):
    print("In get data handler")
    user_id = session.get('user_id')
    print(f"User ID: {user_id}")
    print(f"Option selected: {option}")
    
    if option == 'Combined':
        mortgages = db.connect("SELECT mortgage_id FROM mortgages WHERE user_id = %s", (user_id,))
        if mortgages:
            mortgage_ids = [mortgages[mortgage][0] for mortgage in mortgages]
            data = fetch_mortgage_data(mortgage_ids)
        else:
            data = {"error": "Mortgage not found"}
    else:
        # Find the mortgage by name and get its ID
        mortgage = db.connect("SELECT mortgage_id FROM mortgages WHERE user_id = %s AND mortgage_name = %s", (user_id, option))
        if mortgage:
            mortgage_id = mortgage[0][0]
            print(f"Mortgage selected: {mortgage_id}")
            data = fetch_mortgage_data(mortgage_id)
        else:
            data = {"error": "Mortgage not found"}
            
    print(f"Printing data to update with: {data}")
    print(f"Data type: {type(data)}")
    
    response = jsonify(data)
    print(f"Output: {response.get_json()}")
    
    return response

@app.route('/new_mortgage', methods=['GET', 'POST'])
def new_mortgage():
    error = ""
    mortgage_data = {
        "mortgage_name": "",
        "principal": "",
        "interest_rate": "",
        "deposit": "",
        "start_date": "",
        "extra_costs": "",
        "term": ""
    }
    analysis_summary = None
    graph_div = {"data": [], "layout": {}}  # Initialize graph_div here

    if request.method == 'POST':
        try:
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
                mortgage_data["mortgage_name"],
                mortgage_data["start_date"],
                float(mortgage_data["interest_rate"]),
                int(mortgage_data["term"]),
                float(mortgage_data["principal"]),
                float(mortgage_data["extra_costs"]),
                float(mortgage_data["deposit"])
            )
            
            analysis_summary = mortgage_analysis([mortgage], [], "new_summary", datetime.now())
            graph_json = mortgage_graph([mortgage], [], "Monthly")
            if graph_json:
                graph_div = json.loads(graph_json)
        except Exception as e:
            error = str(e)
    
    return render_template('new_mortgage.html', error=error, mortgage_data=mortgage_data, analysis_result=analysis_summary, graph_div=graph_div)

@app.route('/save_mortgage', methods=['POST'])
def save_mortgage():
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
            mortgage_data["mortgage_name"],
            mortgage_data["start_date"],
            float(mortgage_data["interest_rate"]),
            int(mortgage_data["term"]),
            float(mortgage_data["principal"]),
            float(mortgage_data["extra_costs"]),
            float(mortgage_data["deposit"])
        )

        db.connect("INSERT INTO mortgages (user_id, mortgage_name, estab_date, initial_interest, initial_term, initial_principal, extra_cost, deposit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (user_id, mortgage.mortgageName, mortgage.estabDate, mortgage.initialInterest, mortgage.initialTerm, mortgage.initialPrincipal, mortgage.extraCost, mortgage.deposit))
        
        return redirect(url_for("home"))
    except Exception as e:
        return render_template('new_mortgage.html', error=str(e), mortgage_data=mortgage_data, analysis_result=None, graph_div=None)
    
@app.route('/update_mortgage', methods=['GET', 'POST'])
def update_mortgage():
    user_id = session.get('user_id')
    mortgages = []
    
    try:
        # Fetch all mortgages for the user
        query = "SELECT mortgage_id, mortgage_name FROM mortgages WHERE user_id = %s"
        mortgages = db.connect(query, (user_id,))
        # Convert the result to a list of dictionaries for easier handling in the template
        if isinstance(mortgages, list):
            mortgages = [{'id': row[0], 'name': row[1]} for row in mortgages]
        else:
            mortgages = []  # If an error occurred, set mortgages to an empty list
    except Exception as e:
        print(str(e))

    return render_template('update_mortgage.html', mortgages=mortgages)

@app.route('/get_mortgage_data/<int:mortgage_id>', methods=['GET'])
def get_mortgage_data(mortgage_id):
    user_id = session.get('user_id')
    try:
        # Fetch mortgage data
        temp_mortgage = db.connect("SELECT * FROM mortgages WHERE mortgage_id = %s AND user_id = %s", (mortgage_id, user_id))
        
        # Check if any result was returned
        if not temp_mortgage or len(temp_mortgage) == 0:
            raise ValueError("No mortgage found for the given ID and user.")

        temp_mortgage = temp_mortgage[0]  # Extract the first result
        print("Fetched mortgage data:", temp_mortgage)  # Log fetched mortgage data

        # Ensure estab_date is formatted correctly
        estab_date = temp_mortgage[3]
        print("Original estab_date:", estab_date)
        estim_finish_date = estab_date + relativedelta(years=int(temp_mortgage[5]))
        print("testing1")
        current_date = datetime.now()
        print("testing2")
        
        difference = relativedelta(estim_finish_date, current_date)
        print("testing3")
        remaining_years = difference.years
        print("testing4")
        remaining_months = difference.months
        print("testing5")
        mortgage_estab_date = estab_date.strftime("%Y-%m-%d")
        print("Formatted estab_date:", estab_date)

        # Create Mortgage instance
        mortgage = Mortgage(
            temp_mortgage[2],
            mortgage_estab_date,
            float(temp_mortgage[4]),
            int(temp_mortgage[5]),
            float(temp_mortgage[6]),
            float(temp_mortgage[7]),
            float(temp_mortgage[8])
        )
        print(mortgage)
        
        transactions = []
        temp_transactions = db.connect("SELECT * FROM transactions WHERE mortgage_id = %s ORDER BY transaction_id ASC", (mortgage_id,))
        print(temp_transactions)
        for i in range(len(temp_transactions) - 1):
            temp_transaction = temp_transactions[i]
            transaction = Transaction(
                temp_transaction[2],
                temp_transaction[3],
                temp_transaction[4],
                temp_transaction[5],
                temp_transaction[6],
                temp_transaction[7],
                temp_transaction[8],
                temp_transaction[9],
                temp_transaction[10]
            )
            transactions.append(transaction)

        # Generate analysis summary and graph data
        analysis_summary = mortgage_analysis([mortgage], transactions, "new_summary", datetime.now())
        graph_data = json.loads(mortgage_graph([mortgage], transactions, "Monthly"))

        data = {
            "principal": mortgage.initialPrincipal,
            "interest_rate": mortgage.initialInterest,
            "term_years": remaining_years,
            "term_months": remaining_months,
            "payment_override": 0,
            "balloon_payment": 0,
            "comment": "",
            "graph_data": graph_data,
            "analysis_summary": analysis_summary,  # Changed from summary_html to analysis_summary
            "estab_date": mortgage_estab_date,  # Send establishment date
            "initial_term_years": mortgage.initialTerm,  # Send initial term in years
            "initial_term_months": 0  # Send initial term in months (if applicable)
        }

        print("Response data:", data)  # Log response data
        return jsonify(data)
    except Exception as e:
        print("Error fetching mortgage data:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/update_graph_and_summary', methods=['POST'])
def update_graph_and_summary():
    data = request.json
    print(data)
    user_id = session.get('user_id')
    print("Received data:", data)  # Log received data
    
    try:
        temp_mortgage = db.connect("SELECT * FROM mortgages WHERE mortgage_id = %s AND user_id = %s", (data['mortgage_id'], user_id))
        print(temp_mortgage)
        if not temp_mortgage:
            raise ValueError("No mortgage found for the given ID and user.")
        
        temp_mortgage = temp_mortgage[0]
        mortgage = Mortgage(
            temp_mortgage[2],
            temp_mortgage[3],
            float(temp_mortgage[4]),
            int(temp_mortgage[5]),
            float(temp_mortgage[6]),
            float(temp_mortgage[7]),
            float(temp_mortgage[8])
        )
        print(mortgage)
        
        transactions = []
        # Calculate initial analysis summary without any transactions
        initial_summary = mortgage_analysis([mortgage], [], "new_summary", datetime.now())
        
        temp_transactions = db.connect("SELECT * FROM transactions WHERE mortgage_id = %s ORDER BY transaction_id ASC", (data['mortgage_id'],))
        print(temp_transactions)
        for i in range(len(temp_transactions)):
            temp_transaction = temp_transactions[i]
            transaction = Transaction(
                temp_transaction[2],
                temp_transaction[3],
                temp_transaction[4],
                temp_transaction[5],
                temp_transaction[6],
                temp_transaction[7],
                temp_transaction[8],
                temp_transaction[9],
                temp_transaction[10]
            )
            transactions.append(transaction)
        
        print(type(data['update_date']))
        if data['update_date'] == "":
            print('no date')
            update_date = datetime.now().strftime("%Y-%m-%d")
        else:
            print('date')
            update_date = data['update_date']
        print(update_date)
        print(int(data['term_months']))
        new_transaction = Transaction(
            float(data['principal']),
            float(data['interest_rate']),
            update_date,
            int(data['term_years']),
            int(data['term_months']),
            float(data['payment_override']),
            data['extra_payment_type'],
            float(data['balloon_payment']),
            data['comment']
        )
        print(new_transaction)
 
        transactions.append(new_transaction)
        print(transactions)
        change_summary = mortgage_analysis([mortgage], transactions, "change_summary", datetime.now(), initial_summary)
        print(f"Change Summary: {change_summary}")
        graph_data = mortgage_graph(mortgage, transactions, "Monthly")

        response_data = {
            "graph_data": json.loads(graph_data),
            "summary_html": initial_summary,
            "change_summary": change_summary
        }
        return jsonify(response_data)
    except Exception as e:
        print("Error updating graph and summary:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/save_transaction', methods=['POST'])
def save_transaction():
    try:
        print("here!")
        print(request.form)  # Print the entire form data for debugging

        mortgage_id = request.form["mortgage-id"]
        print(f"mortgage_id: {mortgage_id}")
        
        if request.form["update-date"] == "":
            update_date = datetime.now().strftime("%Y-%m-%d")
        else:
            update_date = request.form["update-date"]
        print(f"update_date: {update_date}")
        
        print(f"principal: {request.form['principal']}")
        print(f"interest-rate: {request.form['interest-rate']}")
        
        transaction = Transaction(
            float(request.form["principal"]),
            float(request.form["interest-rate"]),
            update_date,
            int(request.form["term-years"]),
            int(request.form["term-months"]),
            float(request.form["payment-override"]),
            request.form["extra_payment_type"],
            float(request.form["balloon-payment"]),
            request.form["comment"]
        )
        print(transaction)
        print("test")

        test = db.connect(
            "INSERT INTO transactions (mortgage_id, current_principal, current_interest, start_date, remaining_years, remaining_months, extra_payment, extra_payment_type, balloon_payment, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (mortgage_id, transaction.currentPrincipal, transaction.currentInterest, transaction.startDate, transaction.remainingYears, transaction.remainingMonths, transaction.extraPayment, transaction.extraPaymentType, transaction.balloonPayment, transaction.comment)
        )
        print(test)
        
        return redirect(url_for('home'))
    except Exception as e:
        user_id = session.get('user_id')
        mortgages = db.connect("SELECT mortgage_id, mortgage_name FROM mortgages WHERE user_id = %s", (user_id,))
        return render_template('update_mortgage.html', error=str(e), mortgages=mortgages)

@app.route('/remove_data', methods=['GET', 'POST'])
def remove_data():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        # Fetch mortgages for the current user
        mortgages = db.connect(
            "SELECT mortgage_id, mortgage_name, initial_principal, initial_term FROM mortgages WHERE user_id = %s",
            (user_id,)
        )

        # Fetch transactions for the user's mortgages
        mortgage_ids = tuple(mortgage[0] for mortgage in mortgages)
        if mortgage_ids:
            transactions = db.connect(
                "SELECT t.transaction_id, t.start_date, t.comment, m.mortgage_name "
                "FROM transactions t "
                "JOIN mortgages m ON t.mortgage_id = m.mortgage_id "
                "WHERE t.mortgage_id IN %s",
                (mortgage_ids,)
            )
        else:
            transactions = []

        # Debug prints
        print("Mortgages:", mortgages)
        print("Transactions:", transactions)

        return render_template('remove_data.html', mortgages=mortgages, transactions=transactions)
    elif request.method == 'POST':
        pass

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    try:
        # Delete the transaction from the database
        db.connect("DELETE FROM transactions WHERE transaction_id = %s", (transaction_id,))
        return '', 204  # No Content
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return str(e), 500  # Internal Server Error

@app.route('/delete_mortgage/<int:mortgage_id>', methods=['POST'])
def delete_mortgage(mortgage_id):
    try:
        # Delete the mortgage from the database
        test = db.connect("DELETE FROM mortgages WHERE mortgage_id = %s", (mortgage_id,))
        print(test)
        return '', 204  # No Content
    except Exception as e:
        print(f"Error deleting mortgage: {e}")
        return str(e), 500  # Internal Server Error
    
@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    if request.method == 'GET':
        return render_template('user_settings.html')
    elif request.method == 'POST':
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password == confirm_password and old_password != new_password:
            username = session.get('username')
            user_id = session.get('user_id')
            try:
                db_password = db.connect("SELECT password FROM users WHERE user_id = %s and username = %s",(user_id, username,))
                decrypted_password = db_password[0][0]
                print(isinstance(decrypted_password, tuple))
                print(decrypted_password)
                
                authkey = key.load_key()
                print(authkey)
                cipher_suite = Fernet(authkey)
                print(cipher_suite)
                decrypted_password = cipher_suite.decrypt(bytes(decrypted_password)).decode()
                print(decrypted_password)
                
                if old_password == decrypted_password:
                    encrypted_password = cipher_suite.encrypt(new_password.encode())
                    db.connect("UPDATE users SET password) = %s WHERE username = %s and user_id = %s", (encrypted_password.decode(), username, user_id))
                    return render_template("user_settings.html", error="Successfully updated Password!")
                else:
                    return render_template('user_settings.html', error="Old password is incorrect.")
            except Exception as e:
                return render_template('user_settings.html', error=f"An error occurred: {e}")
        else:
            return render_template('user_settings.html', error="New passwords don't match or are the same as the old password.")
        
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)