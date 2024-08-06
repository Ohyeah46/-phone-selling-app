import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1111",
            database="phone_store"
        )
    except Error as e:
        print(f"Error: '{e}'")
    return connection