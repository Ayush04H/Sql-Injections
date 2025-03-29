# src/app.py
import  db_utils  # Correct import: import module as alias

def display_products(products):
    """Displays product information."""
    if products:
        print("\n--- Products Found ---")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: ${product[3]:.2f}")
    else:
        print("\nNo products found.")

def main():
    """Main application function."""
    while True:
        print("\n--- Product Search ---")
        search_term = input("Enter product name to search (or type 'exit' to quit): ")
        if search_term.lower() == 'exit':
            break

        print(f"\nSearching for: '{search_term}' (Vulnerable Query)...")
        vulnerable_products = db_utils.fetch_product_by_name(search_term) # Call functions using alias
        display_products(vulnerable_products)

        print(f"\nSearching for: '{search_term}' (Safe Query)...") #Demonstrating safe query too for comparison
        safe_products = db_utils.fetch_product_by_name_safe(search_term) # Call functions using alias
        display_products(safe_products)

if __name__ == "__main__":
    main()