root = None
import json
import tkinter as tk
from tkinter import messagebox , simpledialog
from tkinter import ttk
from authentication import verify_user , change_master_password
from encryption import create_key , encrypt_data, decrypt_data
from vault import view_vault , save_data
from password_generator import generate_password_gui

search_entry = None
key=None
show_password = False
editing_index = None
attempts = 3
passwords = []
def login_screen():

    global root
    global password_entry


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

    password_entry.bind("<Return>", lambda event: login())


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
            return

def change_master_screen():

    global root
    global old_entry
    global new_entry
    global confirm_entry

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Old Master Password").pack()

    old_entry= tk.Entry(root, show="*")
    old_entry.pack()

    tk.Label(root, text = " New Master Password ").pack()

    new_entry = tk.Entry(root, show="*")
    new_entry.pack()

    tk.Label(root , text = "Confirm New Master Password").pack()
    confirm_entry = tk.Entry(root, show="*")
    confirm_entry.pack()

    tk.Button(root, text="Change Password", command= change_master_password_gui).pack()

def generate_button():
    try:
        length = int(length_entry.get())
        if length <=0:
            messagebox.showerror("Error", "Enter a valid password length")
            return
    except ValueError:
        messagebox.showerror("Error", "Length must be a number")
        return

    if not (uppercase_var.get() or lowercase_var.get() or digits_var.get() or symbols_var.get()):
        messagebox.showerror("Error", "Select at least one character type")
        return

    result = generate_password_gui(int(length_entry.get()), uppercase_var.get(), lowercase_var.get() , digits_var.get(), symbols_var.get())
    password, strength , entropy = result
    password_entry.delete(0, tk.END)
    password_entry.insert(0 , password)
    strength_label.config(text=f"Strength: {strength}")
    entropy_label.config(text=f"Entropy is: {round(entropy, 2)} bits")

def change_master_password_gui():
    old_password =old_entry.get()
    new_password = new_entry.get()
    confirm_password = confirm_entry.get()

    if new_password != confirm_password:
        messagebox.showerror("Error","New passwords do not match")
        return

    result = change_master_password(old_password, new_password)

    if result:
        messagebox.showinfo("Success", "Master password changed")
        show_menu()
    else :
        messagebox.showerror("Error" , "Wrong old password")

def add_password():
    global website_entry, username_entry, password_entry

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

def live_search(event=None):
    query = search_entry.get().lower()

    for row in table.get_children():
        table.delete(row)

    for password in passwords:

        if(query in password["website"].lower() or query in password["username"].lower()):

            table.insert("",tk.END, values=(password["website"], password["username"], "********"))

def save_new_password(website_entry , username_entry , password_entry , key):
    print("SAVE NEW PASSWORD RUNNING")
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    print("Website: ", website)
    print("Username:",username)
    print("Password:", password)

    encrypted_entry = {"website": encrypt_data(website, key), "username": encrypt_data(username, key), "password": encrypt_data(password, key)}

    try:
        with open("vault.json", "r") as file:
            vault = json.load(file)

    except FileNotFoundError:
        vault = []
    global editing_index
    print("EDITING INDEX", editing_index)
    if editing_index is not None:
        print("Edit index", editing_index)
        print("Vault before " ,vault)
        vault[editing_index]=encrypted_entry
        print("Vault after" , vault)
        editing_index = None
    else:
        print(encrypted_entry)
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
    label.pack(pady=10)

    global table
    global passwords
    passwords = view_vault(key)

    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True)

    global search_entry

    search_canvas = tk.Canvas(root, height=40, highlightthickness=0)
    search_canvas.pack(pady=10)

    search_entry = ttk.Entry(search_canvas , width = 40)
    search_entry_window = search_canvas.create_window(100,20,window=search_entry)

    search_canvas.create_window(120,20, window=search_entry, width=220,height=30)

    clear_button = ttk.Button(search_canvas, text = "X", command=clear_search)
    search_canvas.create_window(260,20,window=clear_button)

    search_entry.bind("<KeyRelease>", live_search)



    table = ttk.Treeview(root,columns=("website", "username", "password"),show="headings")

    table.heading("website", text="website")
    table.heading("username", text="username")
    table.heading("password", text="password")

    table.column("website", width=150)
    table.column("username",width=150)
    table.column("password",width=150)

    table.pack(fill="both", expand=True)

    if not passwords:
        table.insert("","end",values=("No passwords","",""))
    else:
        for entry in passwords:
            table.insert("", "end",values=(entry["website"], entry["username"], "********"))

    button_frame=tk.Frame(root)
    button_frame.pack(pady=10)

    edit_button = tk.Button(button_frame , text="Edit", command= edit_password)
    edit_button.pack(side="left",padx=5)

    delete_button = tk.Button(button_frame, text="Delete", command=delete_password)
    delete_button.pack(side="left", padx=5)

    view_button = tk.Button(button_frame, text="Show", command= view_password)
    view_button.pack(side="left",padx=5)

    copy_button = tk.Button(button_frame, text="Copy",command=copy_password)
    copy_button.pack(side="left", padx=5)

    back_button = tk.Button(button_frame, text = "Back", command=show_menu)
    back_button.pack(side="left", padx=5)

def view_password():
    global show_password

    selected= table.selection()

    if selected:
        item = selected[0]
        values = table.item(item,"values")
        index = table.index(item)
        if show_password:
            table.item(item,values=(values[0],values[1],"********"))
            show_password=False
        else :
            table.item(item,values=(values[0],values[1],passwords[index]["password"]))

            show_password=True

def clear_search():
    search_entry.delete(0, tk.END)
    live_search()

def copy_password():
    selected = table.selection()

    if selected:
        values= table.item(selected[0],"values")

        website= values[0]

        for entry in passwords:
            if entry["website"] == website:
                root.clipboard_clear()
                root.clipboard_append(entry["password"])
                break

def edit_password():
    global editing_index
    selected= table.selection()

    if selected:
        editing_index = table.index(selected[0])
        values = table.item(selected[0],"values")

        add_password()

        website_entry.delete(0,tk.END)
        username_entry.delete(0,tk.END)
        password_entry.delete(0,tk.END)

        website_entry.insert(0,values[0])
        username_entry.insert(0,values[1])
        password_entry.insert(0,values[2])


def delete_password():
    selected = table.selection()

    if selected:
        answer = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?")
        if answer:
            values = table.item(selected[0],"values")

            with open("vault.json", "r") as file:
                vault = json.load(file)

            for entry in vault:
                website = decrypt_data(entry["website"],key)
                username = decrypt_data(entry["username"],key)

                if website == values[0] and username == values[1]:
                    vault.remove(entry)
                    break

            with open("vault.json", "w") as file:
                json.dump(vault, file, indent=4)

            table.delete(selected[0])

def save_generated_password():

    website = simpledialog.askstring("Website","Enter the website:")

    username = simpledialog.askstring("Username","Enter the username:")

    password = password_entry.get()

    if password == "":
        messagebox.showerror("Error","Generate a password first")
        return
    print("SAVE KEY", key)
    save_data(website, username, password , key)

    messagebox.showinfo("Success","Password has been saved")


def generator_screen():
    global password_entry
    global strength_label
    global entropy_label
    global length_entry
    global uppercase_var
    global lowercase_var
    global digits_var
    global symbols_var

    uppercase_var = tk.BooleanVar(value=True)
    lowercase_var = tk.BooleanVar(value=True)
    digits_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar(value=True)

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Password Generator").pack()

    tk.Label(root , text ="Password Length").pack()

    length_entry = tk.Entry(root)
    length_entry.pack()

    tk.Checkbutton(root, text="Uppercase",variable= uppercase_var).pack()
    tk.Checkbutton(root, text = "Lowercase",variable = lowercase_var).pack()
    tk.Checkbutton(root, text = "Digits",variable = digits_var).pack()
    tk.Checkbutton(root, text = "Symbols", variable = symbols_var).pack()

    password_entry = tk.Entry(root, width=40)
    password_entry.pack()

    strength_label = tk.Label(root, text="")
    strength_label.pack()

    entropy_label = tk.Label(root, text="")
    entropy_label.pack()

    tk.Button(root, text ="Generate", command= generate_button).pack()

    tk.Button(root, text ="Save", command= save_generated_password).pack()

    tk.Button(root, text ="Back", command = show_menu).pack()


def lock_vault():
    for widget in root.winfo_children():
        widget.destroy()

    login_screen()

def show_menu():

    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Welcome to your Vault", font=("Arial", 18))
    label.pack(pady=20)

    view_button = tk.Button(root, text="View Passwords", width=20, command=lambda: view_passwords(root))
    view_button.pack(pady=5)

    add_button = tk.Button(root, text="Add Passwords",command = add_password, width=20)
    add_button.pack(pady=5)

    generate_button1 = tk.Button(root, text="Generate Passwords", width=20, command = generator_screen)
    generate_button1.pack(pady=5)

    change_button = tk.Button(root, text="Change Master Password", width=20 , command = change_master_screen)
    change_button.pack(pady=5)

    lock_button = tk.Button(root, text="Lock Vault", width=20 , command = lock_vault)
    lock_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", width=20, command=root.destroy)
    exit_button.pack(pady=5)

