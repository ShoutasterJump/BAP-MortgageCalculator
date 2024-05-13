from cryptography.fernet import Fernet
from classes.User import User
import psycopg2
from psycopg2 import sql

def connect(query, params=None):
    try:
        conn = psycopg2.connect(
            dbname="MortgageCalculator",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        # Check if the command is an insertion/creation query
        if query.lower().startswith("insert"):
            # Return a success flag for insert operations
            return True
        else:
            # For other queries, return the fetched results
            result = cur.fetchall()
            return result
            
    except psycopg2.Error as e:
        # Return error message if the query execution fails
        return f"Error executing query: {e}"
    
    finally:
        cur.close()
        conn.close()