import hashlib
import getpass
from db import create_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    connection = create_connection()
    cursor = connection.cursor()
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    hashed_password = hash_password(password)
    
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND exist = TRUE", (username, hashed_password))
    user = cursor.fetchone()
    if user:
        role = user[4]  # Assuming 'role' is the 5th column
        print(f"Logged in as {role}")
        if role == 'admin':
            admin_menu()
        else:
            visitor_menu()
    else:
        print("Invalid login credentials or user does not exist.")

def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. Add phone")
        print("2. Remove phone")
        print("3. View users")
        print("4. Change user role")
        print("5. Logout")
        choice = input("Select an option: ")
        
        if choice == '1':
            add_phone()
        elif choice == '2':
            remove_phone()
        elif choice == '3':
            view_users()
        elif choice == '4':
            change_user_role()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

def visitor_menu():
    while True:
        print("Visitor Menu:")
        print("1. View phones")
        print("2. Logout")
        choice = input("Select an option: ")
        
        if choice == '1':
            view_phones()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Try again.")

def view_phones():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM phones")
    phones = cursor.fetchall()
    for phone in phones:
        print(f"Name: {phone[1]}, Storage: {phone[2]}GB, RAM: {phone[3]}GB, Processor: {phone[4]}")

def add_phone():
    connection = create_connection()
    cursor = connection.cursor()
    name = input("Phone name: ")
    storage = int(input("Storage (GB): "))
    ram = int(input("RAM (GB): "))
    processor = input("Processor: ")
    
    cursor.execute("INSERT INTO phones (name, storage, ram, processor) VALUES (%s, %s, %s, %s)", (name, storage, ram, processor))
    connection.commit()
    print("Phone added.")

def remove_phone():
    connection = create_connection()
    cursor = connection.cursor()
    phone_id = int(input("Phone ID to remove: "))
    
    cursor.execute("DELETE FROM phones WHERE id = %s", (phone_id,))
    connection.commit()
    print("Phone removed.")

def view_users():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, full_name, username, role FROM users WHERE exist = TRUE")
    users = cursor.fetchall()
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Username: {user[2]}, Role: {user[3]}")

def change_user_role():
    connection = create_connection()
    cursor = connection.cursor()
    user_id = int(input("User ID to change role: "))
    new_role = input("New role (visitor/admin): ")
    
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    connection.commit()
    print("User role updated.")

def register():
    connection = create_connection()
    cursor = connection.cursor()
    full_name = input("Full Name: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    hashed_password = hash_password(password)
    
    cursor.execute("INSERT INTO users (full_name, username, password) VALUES (%s, %s, %s)", (full_name, username, hashed_password))
    connection.commit()
    print("User registered. Default role: visitor.")

def main_menu():
    while True:
        print("Main Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()