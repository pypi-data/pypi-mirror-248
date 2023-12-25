import pymysql
import os 

"""from dotenv import load_dotenv

load_dotenv()"""

admin_db_host = "localhost" #os.getenv('ADMIN_DB_HOST')
admin_db_user = "panda" #os.getenv('ADMIN_DB_USER')
admin_db_password = "Redbull1975!!!" #os.getenv('ADMIN_DB_PASSWORD')

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