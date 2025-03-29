import sqlite3
import os
import random
import string

DB_DIR = "db"  # Define the database directory
DB_PATH = "products.db"  # Path to the database file

def create_database():
    """Creates the SQLite database and tables."""
    sqliteConnection = None  # Initialize outside try block for finally clause
    try:
        # Ensure the 'db' directory exists
        if not os.path.exists(DB_DIR):
            print(f"Creating directory: {DB_DIR}")
            os.makedirs(DB_DIR, exist_ok=True)
        else:
            print(f"Directory '{DB_DIR}' already exists.")

        print(f"Database path (absolute): {os.path.abspath(DB_PATH)}")

        # Check if file exists and permissions (before trying to connect)
        if os.path.exists(DB_PATH):
            print(f"Database file '{DB_PATH}' exists.")
            if os.access(DB_PATH, os.W_OK):
                print(f"Write access to '{DB_PATH}': OK")
            else:
                print(f"WARNING: No write access to '{DB_PATH}'!")
        else:
            print(f"Database file '{DB_PATH}' does not exist. Will be created.")
            if os.access(DB_DIR, os.W_OK):
                print(f"Write access to directory '{DB_DIR}': OK (Should be able to create file)")
            else:
                print(f"WARNING: No write access to directory '{DB_DIR}'! Cannot create database file.")
                return  # Exit if no write access to directory

        print('DB Init - Attempting Connection')
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print('Successfully Connected to SQLite')

        # Create products table (only if it doesn't exist)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL
            )
        """)
        sqliteConnection.commit() # Commit table creation
        print(f"Database '{DB_PATH}' and 'products' table created/verified.")
        cursor.close() # Close cursor after table creation

    except sqlite3.Error as error:
        print('Error occurred - Database/Table Creation: ', error)
    except OSError as e:
        print(f'OS Error during directory/file creation/access: {e}')
        print(f'Error details: {e}')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection for DB/Table Creation closed')

def generate_sample_product_data(num_records):
    """Generates a list of sample product data tuples."""
    products_data = []
    product_categories = ["Electronics", "Home Goods", "Apparel", "Books", "Sports", "Toys"]
    adjectives = ["Awesome", "Fantastic", "Incredible", "Stylish", "Durable", "Portable", "Smart", "Efficient", "Elegant", "Modern"]
    nouns = ["Gadget", "Device", "Item", "Product", "Tool", "Accessory", "Equipment", "Appliance", "Gear", "Supply"]

    for _ in range(num_records):
        category = random.choice(product_categories)
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        product_name = f"{adjective} {category} {noun}"

        description_words = [random.choice(adjectives), category, noun, "for", random.choice(["home", "office", "travel", "gaming", "work"]),
                             "use.", "Features", "include:", random.choice(["high performance", "long battery life", "easy to use", "lightweight design", "advanced technology"])]
        description = " ".join(description_words)

        price = round(random.uniform(10.0, 2000.0), 2)  # Price between $10 and $2000
        products_data.append((product_name, description, price))
    return products_data

def populate_database_with_sample_data(num_records):
    """Populates the 'products' table with sample data."""
    sqliteConnection = None # Initialize outside try block
    try:
        print(f"Attempting to connect to database for population at: {DB_PATH}")
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print('Successfully Connected to SQLite for Data Population')

        sample_data = generate_sample_product_data(num_records)

        cursor.executemany("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", sample_data)
        sqliteConnection.commit() # Commit data insertion
        print(f"Successfully inserted {num_records} sample product records into '{DB_PATH}'.")
        cursor.close() # Close cursor after data insertion

    except sqlite3.Error as error:
        print('Error occurred - Data Population: ', error)
        print(f'Error details: {error}') # Print full error details
    except OSError as e:
        print(f'OS Error during database access for population: {e}')
        print(f'Error details: {e}')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection for Data Population closed')

if __name__ == "__main__":
    create_database()  # Ensure database and table exist
    populate_database_with_sample_data(1500)  # Populate with 1500 records
    print("Database setup and population complete.")