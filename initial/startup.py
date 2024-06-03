from initial.authkey import load_key
import psycopg2
from psycopg2 import sql

print("test")

def initial():
    print("test2")
    # Connect to PostgreSQL (you may need to adjust the connection parameters)
    conn = psycopg2.connect (
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True  # Enable autocommit mode
    print("Connecting to PostgreSQL")

    # Create a cursor object
    cur = conn.cursor()

    # Check if the database exists
    cur.execute(
        "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'MortgageCalculator';"
    )
    database_exists = cur.fetchone()

    # If the database doesn't exist, create it
    if not database_exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("MortgageCalculator")))
        
    print("Database created/connected")

    # Close the current connection
    conn.close()

    # Connect to the newly created database
    conn = psycopg2.connect(
        dbname="MortgageCalculator",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True

    # Create a cursor object
    cur = conn.cursor()

    # Create a table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "users" (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password BYTEA NOT NULL
        );
    """)

    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "mortgages" (
            mortgage_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            mortgage_name VARCHAR(40),
            estab_date TIMESTAMP NOT NULL,
            initial_interest DECIMAL NOT NULL,
            initial_term INTEGER NOT NULL,
            initial_principal INTEGER NOT NULL,
            extra_cost DECIMAL,
            deposit INTEGER NOT NULL
        );
    """)

    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "transactions" (
            transaction_id SERIAL PRIMARY KEY,
            mortgage_id INTEGER REFERENCES mortgages(mortgage_id),
            current_principal DECIMAL NOT NULL,
            current_interest DECIMAL NOT NULL,
            start_date TIMESTAMP NOT NULL,
            extra_payment DECIMAL,
            extra_payment_type VARCHAR(11) NOT NULL,
            ballon_payment INTEGER,
            comment TEXT
        );
    """)

    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    load_key()

initial()