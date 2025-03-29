# src/streamlit_app.py
import streamlit as st
import src.db_utils as db_utils  # Import db_utils from src directory

def display_products_streamlit(products, query_type, sql_query=None): # Added sql_query parameter
    """Displays product information in Streamlit, with query type heading and SQL query."""
    st.subheader(f"{query_type} Results") # Subheader for query type

    if sql_query: # Display SQL query if provided
        st.code(sql_query, language="sql") # Use st.code to display SQL nicely

    if products:
        product_data = []
        for product in products:
            product_data.append({
                "ID": product[0],
                "Name": product[1],
                "Description": product[2],
                "Price": f"${product[3]:.2f}"
            })
        st.dataframe(product_data) # Display as a dataframe for better readability
    else:
        st.write("No products found.")
    st.markdown("---") # Separator line

def main():
    st.title("SQL Injection Demo - Product Search")
    st.markdown("This application demonstrates **SQL Injection vulnerability** in the 'Vulnerable Query' vs. the 'Safe Query' using parameterized queries.")
    st.markdown("**Instructions:** Enter a product name or an SQL Injection payload in the text box below to see the difference in results between the vulnerable and safe queries.")

    search_term = st.text_input("Enter product name or SQL Injection payload to search:", "")

    if search_term:
        st.write(f"Searching for: **'{search_term}'**")

        st.write("### Vulnerable Query Results:")
        st.error("This query is **VULNERABLE to SQL Injection**. User input is directly embedded into the SQL query string.") # Use st.error to highlight vulnerability
        vulnerable_products = db_utils.fetch_product_by_name(search_term)
        # Get the actual query string from db_utils (you might need to modify db_utils to return it or capture it)
        # For now, just reconstruct a basic example for display
        example_vulnerable_query = f"SELECT * FROM products WHERE name = '{search_term}'"
        display_products_streamlit(vulnerable_products, "Vulnerable Query (INJECTED)", sql_query=example_vulnerable_query) # Pass sql_query


        st.write("### Safe Query Results:")
        st.success("This query is **SAFE from SQL Injection**. It uses parameterized queries, which prevent user input from being interpreted as SQL code.") # Use st.success to highlight safety
        safe_products = db_utils.fetch_product_by_name_safe(search_term)
        # Similar to vulnerable query, reconstruct a basic example for display
        example_safe_query = "SELECT * FROM products WHERE name = ?" # Parameterized query structure
        display_products_streamlit(safe_products, "Safe Query (Parameterized)", sql_query=example_safe_query) # Pass sql_query


if __name__ == "__main__":
    main()