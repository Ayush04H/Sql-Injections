# src/db_utils.py
import sqlite3
import os

DB_PATH = r"D:\Cyber_security\db\products.db"  # Absolute path to database

def connect_db():
    """Connects to the SQLite database."""
    try:
        print(f"Attempting to connect to database at (Absolute Path): {DB_PATH}") # Debug print for absolute path
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def fetch_product_by_name(product_name):
    """Fetches products from the database based on the product name (VULNERABLE TO SQL INJECTION)."""
    conn = connect_db()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        # Vulnerable query - directly embedding user input
        query = f"SELECT * FROM products WHERE name = '{product_name}'"
        print(f"Executing Vulnerable Query (INJECTED): {query}") # Print vulnerable query with label
        cursor.execute(query)
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return None
    finally:
        conn.close()

# Example of a function using parameterized query (SQL Injection safe)
def fetch_product_by_name_safe(product_name):
    """Fetches products using parameterized queries (SQL Injection safe)."""
    conn = connect_db()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE name = ?" # Placeholder ?
        print(f"Executing Safe Query (Parameterized): SELECT * FROM products WHERE name = ?  with parameter: {product_name}") # Print safe query info
        cursor.execute(query, (product_name,)) # Pass user input as a tuple
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return None
    finally:
        conn.close()