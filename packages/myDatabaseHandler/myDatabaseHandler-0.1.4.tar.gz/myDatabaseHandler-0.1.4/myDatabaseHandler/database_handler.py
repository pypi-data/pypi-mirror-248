import pymysql
import os 

"""from dotenv import load_dotenv

load_dotenv()"""

admin_db_host = "localhost"
admin_db_user =  "panda"
admin_db_password = "Redbull1975!!!"


host = "localhost"
username =  "panda"
password = "Redbull1975!!!"

"""
admin_db_host = os.getenv('ADMIN_DB_HOST')
admin_db_user =  os.getenv('ADMIN_DB_USER')
admin_db_password = os.getenv('ADMIN_DB_PASSWORD')
"""

# Function to establish a database connection
def connect_to_database(database):
    return pymysql.connect(
        host=admin_db_host,
        user=admin_db_user,
        password=admin_db_password,
        db=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

# Function to execute SQL queries and fetch data
def execute_sql_query(database, query, params=None):
    connection = connect_to_database(database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        connection.commit()  # Commit the changes to the database
    finally:
        connection.close()
    return result

def getCssStyling(platform):
    platform = platform
    # Assuming your SQL query to fetch data from the product_table is something like this
    query = f"SELECT cssClassXRC, cssClassXRB FROM product_table WHERE platform = '{platform}'"
    
    # Call execute_sql_query function to fetch data
    cssStyling = execute_sql_query("products", query)
    
    # Assuming execute_sql_query returns a list of dictionaries, take the first one
    return cssStyling[0] if cssStyling else None

def getSingleValue(column, database, table, username,):
    try:
        # Using placeholders for security to prevent SQL injection
        select_query = f"SELECT {column} FROM {table} WHERE username = %s"

        # Assuming execute_sql_query is a function that takes a query, table name, and parameters
        result = execute_sql_query(database, select_query, (username,))

        if result:
            # Log the result for debugging
            print("Result from the database:", result)

            # Check if the result is a list with at least one dictionary
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                # Check if the column key exists in the first dictionary
                if column in result[0]:
                    # Log the extracted value for debugging
                    print(f"Extracted value for platform '{column}': {result[0][column]}")
                    return result[0][column]
                else:
                    print(f"Platform '{column}' not found in the result dictionary.")
            else:
                print("Invalid result format. Expected a list with at least one dictionary.")
        else:
            print(f"No result found in the database for username '{username}'.")

        return None  # or any default value you prefer
    except:
        return None
    
    
    
    
    
    
    
    
    
    
    
# KICKBOOST UTILS


def perform_database_operation_message_prompt(database, table, colum2name, operation, **kwargs):
    # Establish a connection to the database
    connection = pymysql.connect(host=host, user=username, password=password, db=database)
    # SQL statement to create the table
    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Check if the table exists for "add" and "update" operations, and create it if necessary
        if operation == "add" or operation == "update":
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table} (id INT AUTO_INCREMENT PRIMARY KEY, {colum2name} VARCHAR(255))"
            cursor.execute(create_table_query)

        # Perform the requested operation
        if operation == "add":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            columns = ', '.join(kwargs.keys())
            values = ', '.join(['%s'] * len(kwargs.values()))
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(kwargs.values()))
            

        elif operation == "delete":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            conditions = ' AND '.join([f"{key} = %s" for key in kwargs.keys()])
            query = f"DELETE FROM {table} WHERE {conditions}"
            cursor.execute(query, tuple(kwargs.values()))

        elif operation == "update":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            columns_values = ', '.join([f"{key} = %s" for key in kwargs.keys()])
            query = f"UPDATE {table} SET {columns_values}"
            cursor.execute(query, tuple(kwargs.values()))

        elif operation == "select":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            conditions = ' AND '.join([f"{key} = %s" for key in kwargs.keys()])
            query = f"SELECT * FROM {table} WHERE {conditions}"
            cursor.execute(query, tuple(kwargs.values()))
            rows = cursor.fetchall()
            return rows

        else:
            print("Invalid operation. Please choose from 'add', 'delete', 'update', or 'select'.")

        # Commit the changes to the database
        connection.commit()

    except pymysql.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()




def perform_database_operation(database, table, operation, **kwargs):
    # Establish a connection to the database
    connection = pymysql.connect(host=host, user=username, password=password, db=database)
    # SQL statement to create the table
    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Perform the requested operation
        if operation == "add":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            columns = ', '.join(kwargs.keys())
            values = ', '.join(['%s'] * len(kwargs.values()))
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(kwargs.values()))
            

        elif operation == "delete":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            conditions = ' AND '.join([f"{key} = %s" for key in kwargs.keys()])
            query = f"DELETE FROM {table} WHERE {conditions}"
            cursor.execute(query, tuple(kwargs.values()))

        elif operation == "update":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            columns_values = ', '.join([f"{key} = %s" for key in kwargs.keys()])
            query = f"UPDATE {table} SET {columns_values}"
            cursor.execute(query, tuple(kwargs.values()))

        elif operation == "select":
            # Example: kwargs = {"column1": "value1", "column2": "value2"}
            conditions = ' AND '.join([f"{key} = %s" for key in kwargs.keys()])
            query = f"SELECT * FROM {table} WHERE {conditions}"
            cursor.execute(query, tuple(kwargs.values()))
            rows = cursor.fetchall()
            return rows

        else:
            print("Invalid operation. Please choose from 'add', 'delete', 'update', or 'select'.")

        # Commit the changes to the database
        connection.commit()

    except pymysql.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def perform_database_operation_all(database, table, operation, columns=None, conditions=None):
    # Create a MySQL connection
    db_config = {
        'host': admin_db_host,
        'user': admin_db_user,
        'password': admin_db_password,
        'database': database
    }
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Construct the SQL query based on the operation
            if operation == 'select':
                # Construct the SELECT query
                select_query = f"SELECT {', '.join(columns)} FROM {table}"
                if conditions:
                    where_clause = ' AND '.join(f"{column} = %s" for column in conditions.keys())
                    select_query += f" WHERE {where_clause}"
                    cursor.execute(select_query, tuple(conditions.values()))
                else:
                    cursor.execute(select_query)
                result = cursor.fetchall()
                return result
            elif operation == 'insert':
                # Construct the INSERT query
                insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                cursor.execute(insert_query, tuple(columns.values()))
                connection.commit()
    finally:
        connection.close()


def increment_column_value(column, increment):
    # Connect to the database
    connection = pymysql.connect(
        host=admin_db_host,  # Replace with the actual database host
        user=admin_db_user,  # Replace with your MySQL username
        password=admin_db_password,  # Replace with your MySQL password
        database='stats'
    )

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Increment the value in the specified column by the given increment
        query = f"UPDATE stats SET {column} = {column} + {increment}"
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

        print(f"{column} incremented by {increment} successfully!")
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and the database connection
        cursor.close()
        connection.close()


def check_database(username, value, column):
    # Create a MySQL connection
    db_connection = pymysql.connect(
        host=admin_db_host,
        user=admin_db_user,
        password=admin_db_password,
        database='users'
    )

    # Fetch views for the given username
    cursor = db_connection.cursor()
    cursor.execute(f"SELECT {column} FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data is None:
        return "User not found."

    user_views = user_data[0]
    
    # Convert value to int before comparing
    value = int(value)

    if value > user_views:
        return "YOU'RE NOT ALLOWED TO DO THIS"
    
    else:
        # Subtract the value from user's views
        new_data = user_views - value
        cursor.execute(f"UPDATE users SET {column} = %s WHERE username = %s", (new_data, username,))
        db_connection.commit()
        cursor.close()
        increment_column_value(column, value)
        return f"Successfully started! You have {str(new_data)} left!"
    