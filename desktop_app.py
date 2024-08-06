import tkinter as tk
from tkinter import messagebox
from db import create_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class PhoneStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Store")

        self.login_frame = tk.Frame(root)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s AND exist = TRUE", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            role = user[0]
            self.open_role_frame(role)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or user does not exist.")

    def open_role_frame(self, role):
        self.login_frame.pack_forget()
        if role == 'admin':
            AdminFrame(self.root)
        else:
            VisitorFrame(self.root)

    def register(self):
        RegisterWindow(self.root)

class AdminFrame:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.add_phone_button = tk.Button(self.frame, text="Add Phone", command=self.add_phone)
        self.add_phone_button.pack()

        self.remove_phone_button = tk.Button(self.frame, text="Remove Phone", command=self.remove_phone)
        self.remove_phone_button.pack()

        self.view_users_button = tk.Button(self.frame, text="View Users", command=self.view_users)
        self.view_users_button.pack()

        self.change_role_button = tk.Button(self.frame, text="Change User Role", command=self.change_user_role)
        self.change_role_button.pack()

    def add_phone(self):
        # Implement adding phone functionality
        pass

    def remove_phone(self):
        # Implement removing phone functionality
        pass

    def view_users(self):
        # Implement viewing users functionality
        pass

    def change_user_role(self):
        # Implement changing user role functionality
        pass

class VisitorFrame:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.view_phones_button = tk.Button(self.frame, text="View Phones", command=self.view_phones)
        self.view_phones_button.pack()

    def view_phones(self):
        # Implement viewing phones functionality
        pass

class RegisterWindow:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Register")

        tk.Label(self.top, text="Full Name").pack()
        self.full_name_entry = tk.Entry(self.top)
        self.full_name_entry.pack()

        tk.Label(self.top, text="Username").pack()
        self.username_entry = tk.Entry(self.top)
        self.username_entry.pack()

        tk.Label(self.top, text="Password").pack()
        self.password_entry = tk.Entry(self.top, show="*")
        self.password_entry.pack()

        tk.Button(self.top, text="Register", command=self.register).pack()

    def register(self):
        full_name = self.full_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (full_name, username, password) VALUES (%s, %s, %s)", (full_name, username, hashed_password))
        connection.commit()

        messagebox.showinfo("Registration Successful", "User registered successfully.")
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneStoreApp(root)
    root.mainloop()