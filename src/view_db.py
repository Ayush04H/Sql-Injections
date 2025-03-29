import sqlite3
import os

DB_DIR = "db"  # Assuming 'db' directory is in the same location as the script or relative to it
DB_PATH = os.path.join(DB_DIR, "products.db")

def view_database_data():
    """Connects to the products.db database and prints the first 50 rows of data from the products table."""
    sqliteConnection = None
    try:
        print(f"Attempting to connect to database at: {DB_PATH}")
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print('Successfully Connected to SQLite')

        # Fetch column names (headers)
        cursor.execute("PRAGMA table_info(products)")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info] # Index 1 has column name

        # Fetch the first 50 rows of data from the products table
        cursor.execute("SELECT * FROM products LIMIT 50")  # Added LIMIT 50 here
        records = cursor.fetchall()

        if not records:
            print("\nNo data found in the 'products' table.")
            return

        # Print headers
        header_row = "| " + " | ".join(column_names) + " |"
        separator_line = "+" + "-+-".join(["-" * (len(col)) for col in column_names]) + "+" # Simple separator
        print("\n" + separator_line)
        print(header_row)
        print(separator_line)

        # Print data rows
        for row in records:
            data_row = "| " + " | ".join(map(str, row)) + " |" # Convert each item in row to string
            print(data_row)
        print(separator_line + "\n")

    except sqlite3.Error as error:
        print('Error occurred while viewing database data: ', error)
        print(f'Error details: {error}')
    except OSError as e:
        print(f'OS Error during database access: {e}')
        print(f'Error details: {e}')
    finally:
        if sqliteConnection:
            cursor.close() # Close cursor
            sqliteConnection.close() # Close connection
            print('SQLite Connection closed')

if __name__ == "__main__":
    view_database_data()