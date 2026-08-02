import json
import tkinter as tk
from tkinter import messagebox
from authentication import verify_user
from encryption import create_key , encrypt_data, decrypt_data
from vault import view_vault , save_data
key=None
attempts = 3

def login_screen():

    global root
    global password_entry

    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("400x300")

    title_label = tk.Label(root, text = "Password Manager", font = ("Arial", 18))
    title_label.pack(pady=20)

    password_label = tk.Label(root, text = "Master Password: ")
    password_label.pack()

    password_entry = tk.Entry(root,show="*" , width = 30)
    password_entry.pack(pady=10)

    login_button = tk.Button(root, text = "Login", command = login)
    login_button.pack(pady=10)

    root.bind("<Return>", lambda event: login())
    root.mainloop()

def login():
    global attempts
    global key

    password =  password_entry.get()

    logged_in= verify_user(password)
    if logged_in:
        key = create_key(password)
        show_menu()

    else:
        attempts -= 1

        messagebox.showerror("Login Failed",f"Attempts left :{attempts} ")

        if attempts == 0:
            root.destroy()

def add_password():

    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root, text = "Add new password", font = ("Arial", 16))
    title.pack(pady=20)

    website_label = tk.Label(root, text = "Website: ", font = ("Arial", 16))
    website_label.pack()

    website_entry = tk.Entry(root)
    website_entry.pack()

    username_label = tk.Label(root, text = "Username:", font = ("Arial", 16))
    username_label.pack()

    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text = "Password: ", font = ("Arial", 16))
    password_label.pack()

    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    save_button = tk.Button(root, text = "Save", command =lambda: save_new_password(website_entry, username_entry, password_entry,key))
    save_button.pack(pady=10)

    back_button = tk.Button(root, text = "Back", command= show_menu)
    back_button.pack()

def save_new_password(website_entry , username_entry , password_entry , key):

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    encrypted_entry = {"website": encrypt_data(website, key), "username": encrypt_data(username, key), "password": encrypt_data(password, key)}

    try:
        with open("vault.json", "r") as file:
            vault = json.load(file)

    except FileNotFoundError:
        vault = []

    vault.append(encrypted_entry)

    with open("vault.json", "w") as file:
        json.dump(vault, file, indent=4)

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def view_passwords(root):
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text = "Your saved passwords", font = ("Arial", 16))
    label.pack(pady=20)

    passwords = view_vault(key)

    if not passwords:
        empty = tk.Label(root, text="Vault is empty")
        empty.pack()
    else:
        for entry in passwords:
            label = tk.Label(root, text =f"Website: {entry['website']}\nUsername: {entry['username']}\nPassword: {entry['password']}", font = ("Arial", 16))
            label.pack(pady=10)
    back_button = tk.Button(root, text = "Back", command=show_menu)
    back_button.pack(pady=10)

def show_menu():

    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Welcome to your Vault", font=("Arial", 18))
    label.pack(pady=20)

    view_button = tk.Button(root, text="View Passwords", width=20, command=lambda: view_passwords(root))
    view_button.pack(pady=5)

    search_button = tk.Button(root, text="Search Passwords", width=20)
    search_button.pack(pady=5)

    add_button = tk.Button(root, text="Add Passwords",command = add_password, width=20)
    add_button.pack(pady=5)

    edit_button = tk.Button(root, text="Edit Passwords", width=20)
    edit_button.pack(pady=5)

    generate_button = tk.Button(root, text="Generate Passwords", width=20)
    generate_button.pack(pady=5)

    change_button = tk.Button(root, text="Change Master Password", width=20)
    change_button.pack(pady=5)

    lock_button = tk.Button(root, text="Lock Vault", width=20)
    lock_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", width=20, command=root.destroy)
    exit_button.pack(pady=5)


