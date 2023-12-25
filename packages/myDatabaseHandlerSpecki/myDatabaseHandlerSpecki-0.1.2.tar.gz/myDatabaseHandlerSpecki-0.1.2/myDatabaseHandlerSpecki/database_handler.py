import pymysql
import os 
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('CUSTOMER_DB_HOST')
db_user = os.getenv('CUSTOMER_DB_USER')
db_password = os.getenv('CUSTOMER_DB_PASSWORD')
db_name = os.getenv('CUSTOMER_DB_NAME')

socket_db_host = os.getenv('SOCKET_DB_HOST')
socket_db_user = os.getenv('SOCKET_DB_USER')
socket_db_password = os.getenv('SOCKET_DB_PASSWORD')
socket_db_name = os.getenv('SOCKET_DB_NAME')

admin_db_host = os.getenv('ADMIN_DB_HOST')
admin_db_user = os.getenv('ADMIN_DB_USER')
admin_db_password = os.getenv('ADMIN_DB_PASSWORD')
admin_db_name = os.getenv('ADMIN_DB_NAME')

shortener_db_host = os.getenv('SHORTENER_DB_HOST')
shortener_db_user = os.getenv('SHORTENER_DB_USER')
shortener_db_password = os.getenv('SHORTENER_DB_PASSWORD')
shortener_db_name = os.getenv('SHORTENER_DB_NAME')

# Connect to admin database
def admin_connect_database(database):
    return pymysql.connect(
        host=admin_db_host,
        user=admin_db_user,
        password=admin_db_password,
        db=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

# Function to execute SQL queries and fetch data
def execute_admin_sql_query(database, query, params=None):
    connection = admin_connect_database(database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result

# Connect to admin database
def socket_connect_database(database):
    return pymysql.connect(
        host=socket_db_host,
        user=socket_db_user,
        password=socket_db_password,
        db=socket_db_name,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

# Function to execute SQL queries and fetch data
def execute_socket_sql_query(database, query, params=None):
    connection = socket_connect_database(database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result

# Connect to customer database
def customer_connect_database(database):
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    
# Function to execute SQL queries and fetch data
def execute_customer_sql_query(database, query, params=None):
    connection = customer_connect_database(database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result

def shortener_connect_database(database):
    return pymysql.connect(
        host=shortener_db_host,
        user=shortener_db_user,
        password=shortener_db_password,
        db=shortener_db_name,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    
# Function to execute SQL queries and fetch data
def execute_shortener_sql_query(database, query, params=None):
    connection = shortener_connect_database(database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result
