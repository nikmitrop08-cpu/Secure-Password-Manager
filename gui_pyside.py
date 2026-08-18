
import sys
import os
import json

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout
)

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from authentication import (
    verify_user,
    create_master_password,
    master_password_exists,
    change_master_password
)

from encryption import create_key, encrypt_data
from vault import view_vault, save_data
from password_generator import generate_password_gui


# =========================
# GLOBAL VARIABLES
# =========================

window = None

key = None

attempts = 3

password_entry = None


# =========================
# ICON SYSTEM
# =========================

def icon_path(name):
    return os.path.join(
        "icons",
        name
    )


# =========================
# MAIN WINDOW
# =========================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Secure Password Manager"
        )

        self.resize(
            900,
            600
        )

        self.setWindowIcon(
            QIcon(
                icon_path("lock.svg")
            )
        )

        self.container = QWidget()

        self.setCentralWidget(
            self.container
        )

        self.layout = QVBoxLayout()

        self.layout.setAlignment(
            Qt.AlignCenter
        )

        self.container.setLayout(
            self.layout
        )

        self.setStyleSheet("""

        QMainWindow {
            background-color: #080b12;
        }

        QWidget {
            background-color: #080b12;
            color: white;
            font-family: Arial;
            font-size: 14px;
        }

        QLabel {
            color: #00A8FF;
            font-size: 16px;
        }

        QPushButton {
            background-color: #001f3f;
            color: #00A8FF;
            border: 1px solid #00A8FF;
            border-radius: 8px;
            padding: 10px;
            min-width: 180px;
        }

        QPushButton:hover {
            background-color: #003366;
            color: #00FFFF;
        }

        QLineEdit {
            background-color: #111827;
            color: white;
            border: 1px solid #00A8FF;
            border-radius: 6px;
            padding: 8px;
            min-width: 250px;
        }

        """)


# =========================
# CLEAR WINDOW
# =========================

def clear_screen():

    while window.layout.count():

        item = window.layout.takeAt(0)

        widget = item.widget()

        if widget:
            widget.deleteLater()


# =========================
# START APP
# =========================

def startapp():

    global window

    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    window = MainWindow()

    if master_password_exists():
        login_screen()

    else:
        create_master_password_gui()

    window.show()

    app.exec()


# =========================
# LOGIN SCREEN
# =========================

def login_screen():

    global password_entry

    clear_screen()

    title = QLabel(
        "Secure Password Manager"
    )

    title.setAlignment(
        Qt.AlignCenter
    )

    window.layout.addWidget(
        title
    )

    label = QLabel(
        "Master Password"
    )

    window.layout.addWidget(
        label
    )

    password_entry = QLineEdit()

    password_entry.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        password_entry
    )

    button = QPushButton(
        "Login"
    )

    button.setIcon(
        QIcon(
            icon_path("lock.svg")
        )
    )

    button.clicked.connect(
        login
    )

    window.layout.addWidget(
        button
    )


# =========================
# LOGIN FUNCTION
# =========================

def login():

    global attempts
    global key

    password = password_entry.text()

    if verify_user(password):

        key = create_key(password)

        show_menu()

    else:

        attempts -= 1

        QMessageBox.critical(
            window,
            "Login Failed",
            f"Attempts left: {attempts}"
        )

        if attempts == 0:
            window.close()


# =========================
# CREATE MASTER PASSWORD
# =========================

def create_master_password_gui():

    clear_screen()

    title = QLabel(
        "Create Master Password"
    )

    title.setAlignment(
        Qt.AlignCenter
    )

    window.layout.addWidget(
        title
    )

    password = QLineEdit()

    password.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        password
    )

    confirm = QLineEdit()

    confirm.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        confirm
    )

    button = QPushButton(
        "Create"
    )

    button.clicked.connect(
        lambda:
        create(password, confirm)
    )

    window.layout.addWidget(
        button
    )


def create(password, confirm):

    if password.text() != confirm.text():

        QMessageBox.warning(
            window,
            "Error",
            "Passwords do not match"
        )

        return

    create_master_password(
        password.text()
    )

    QMessageBox.information(
        window,
        "Success",
        "Master password created"
    )

    login_screen()


# =========================
# MAIN MENU
# =========================

def show_menu():

    clear_screen()

    title = QLabel(
        "Welcome to your Vault"
    )

    title.setAlignment(
        Qt.AlignCenter
    )

    window.layout.addWidget(
        title
    )

    view_button = QPushButton(
        "View Passwords"
    )

    view_button.clicked.connect(
        view_passwords
    )

    window.layout.addWidget(
        view_button
    )

    add_button = QPushButton(
        "Add Password"
    )

    add_button.setIcon(
        QIcon(
            icon_path("copy.svg")
        )
    )

    add_button.clicked.connect(
        add_password
    )

    window.layout.addWidget(
        add_button
    )

    generator_button = QPushButton(
        "Generate Password"
    )

    generator_button.clicked.connect(
        generator_screen
    )

    window.layout.addWidget(
        generator_button
    )

    change_button = QPushButton(
        "Change Master Password"
    )

    change_button.setIcon(
        QIcon(
            icon_path("settings.svg")
        )
    )

    change_button.clicked.connect(
        change_master_screen
    )

    window.layout.addWidget(
        change_button
    )

    lock_button = QPushButton(
        "Lock Vault"
    )

    lock_button.setIcon(
        QIcon(
            icon_path("lock.svg")
        )
    )

    lock_button.clicked.connect(
        lock_vault
    )

    window.layout.addWidget(
        lock_button
    )

    exit_button = QPushButton(
        "Exit"
    )

    exit_button.clicked.connect(
        window.close
    )

    window.layout.addWidget(
        exit_button
    )


# =========================
# LOCK VAULT
# =========================

def lock_vault():

    login_screen()


# =========================
# ADD PASSWORD
# =========================

website_entry = None
username_entry = None
new_password_entry = None


def add_password():

    global website_entry
    global username_entry
    global new_password_entry

    clear_screen()

    title = QLabel(
        "Add New Password"
    )

    window.layout.addWidget(
        title
    )

    website_entry = QLineEdit()

    website_entry.setPlaceholderText(
        "Website"
    )

    window.layout.addWidget(
        website_entry
    )

    username_entry = QLineEdit()

    username_entry.setPlaceholderText(
        "Username"
    )

    window.layout.addWidget(
        username_entry
    )

    new_password_entry = QLineEdit()

    new_password_entry.setPlaceholderText(
        "Password"
    )

    new_password_entry.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        new_password_entry
    )

    save_button = QPushButton(
        "Save"
    )

    save_button.clicked.connect(
        save_new_password
    )

    window.layout.addWidget(
        save_button
    )

    back_button = QPushButton(
        "Back"
    )

    back_button.clicked.connect(
        show_menu
    )

    window.layout.addWidget(
        back_button
    )


def save_new_password():

    website = website_entry.text()

    username = username_entry.text()

    password = new_password_entry.text()

    encrypted = encrypt_data(
        password,
        key
    )

    data = {

        "website": website,

        "username": username,

        "password": encrypted

    }

    try:

        with open(
            "vault.json",
            "r"
        ) as file:

            vault = json.load(file)

    except FileNotFoundError:

        vault = []

    vault.append(
        data
    )

    with open(
        "vault.json",
        "w"
    ) as file:

        json.dump(
            vault,
            file,
            indent=4
        )

    QMessageBox.information(
        window,
        "Success",
        "Password saved"
    )


# =========================
# CHANGE MASTER PASSWORD
# =========================

old_entry = None
new_entry = None
confirm_entry = None


def change_master_screen():

    global old_entry
    global new_entry
    global confirm_entry

    clear_screen()

    old_entry = QLineEdit()

    old_entry.setPlaceholderText(
        "Old password"
    )

    old_entry.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        old_entry
    )

    new_entry = QLineEdit()

    new_entry.setPlaceholderText(
        "New password"
    )

    new_entry.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        new_entry
    )

    confirm_entry = QLineEdit()

    confirm_entry.setPlaceholderText(
        "Confirm new password"
    )

    confirm_entry.setEchoMode(
        QLineEdit.Password
    )

    window.layout.addWidget(
        confirm_entry
    )

    button = QPushButton(
        "Change Password"
    )

    button.clicked.connect(
        change_password
    )

    window.layout.addWidget(
        button
    )


def change_password():

    if new_entry.text() != confirm_entry.text():

        QMessageBox.warning(
            window,
            "Error",
            "Passwords do not match"
        )

        return

    result = change_master_password(
        old_entry.text(),
        new_entry.text()
    )

    if result:

        QMessageBox.information(
            window,
            "Success",
            "Password changed"
        )

        show_menu()

    else:

        QMessageBox.warning(
            window,
            "Error",
            "Wrong old password"
        )


# =========================
# PASSWORD GENERATOR
# =========================

length_entry = None
generated_password_entry = None
strength_label = None
entropy_label = None

uppercase_checkbox = None
lowercase_checkbox = None
digits_checkbox = None
symbols_checkbox = None


def generate_password_button():

    try:

        length = int(
            length_entry.text()
        )

        if length <= 0:
            raise ValueError

    except ValueError:

        QMessageBox.warning(
            window,
            "Invalid Length",
            "Enter a valid positive password length."
        )

        return

    uppercase = uppercase_checkbox.isChecked()
    lowercase = lowercase_checkbox.isChecked()
    digits = digits_checkbox.isChecked()
    symbols = symbols_checkbox.isChecked()

    if not any([
        uppercase,
        lowercase,
        digits,
        symbols
    ]):

        QMessageBox.warning(
            window,
            "No Character Types",
            "Select at least one character type."
        )

        return

    required_categories = sum([
        uppercase,
        lowercase,
        digits,
        symbols
    ])

    if length < required_categories:

        QMessageBox.warning(
            window,
            "Length Too Short",
            "Password length is too short for the selected character types."
        )

        return

    password, strength, entropy = generate_password_gui(
        length,
        uppercase,
        lowercase,
        digits,
        symbols
    )

    generated_password_entry.setText(
        password
    )

    strength_label.setText(
        f"Strength: {strength}"
    )

    entropy_label.setText(
        f"Entropy: {entropy:.2f} bits"
    )


def generator_screen():

    global length_entry
    global generated_password_entry
    global strength_label
    global entropy_label

    global uppercase_checkbox
    global lowercase_checkbox
    global digits_checkbox
    global symbols_checkbox

    clear_screen()

    title = QLabel(
        "Password Generator"
    )

    window.layout.addWidget(
        title
    )

    length_entry = QLineEdit()

    length_entry.setPlaceholderText(
        "Password length"
    )

    window.layout.addWidget(
        length_entry
    )

    uppercase_checkbox = QCheckBox(
        "Uppercase"
    )

    uppercase_checkbox.setChecked(
        True
    )

    window.layout.addWidget(
        uppercase_checkbox
    )

    lowercase_checkbox = QCheckBox(
        "Lowercase"
    )

    lowercase_checkbox.setChecked(
        True
    )

    window.layout.addWidget(
        lowercase_checkbox
    )

    digits_checkbox = QCheckBox(
        "Numbers"
    )

    digits_checkbox.setChecked(
        True
    )

    window.layout.addWidget(
        digits_checkbox
    )

    symbols_checkbox = QCheckBox(
        "Symbols"
    )

    symbols_checkbox.setChecked(
        True
    )

    window.layout.addWidget(
        symbols_checkbox
    )

    generated_password_entry = QLineEdit()

    generated_password_entry.setReadOnly(
        True
    )

    window.layout.addWidget(
        generated_password_entry
    )

    strength_label = QLabel(
        ""
    )

    window.layout.addWidget(
        strength_label
    )

    entropy_label = QLabel(
        ""
    )

    window.layout.addWidget(
        entropy_label
    )

    generate_button = QPushButton(
        "Generate"
    )

    generate_button.clicked.connect(
        generate_password_button
    )

    window.layout.addWidget(
        generate_button
    )

    back = QPushButton(
        "Back"
    )

    back.clicked.connect(
        show_menu
    )

    window.layout.addWidget(
        back
    )


# =========================
# VAULT TABLE
# =========================

passwords = []

table = None

showing_password = False


def view_passwords():

    global table
    global passwords

    clear_screen()

    title = QLabel(
        "Your Saved Passwords"
    )

    window.layout.addWidget(
        title
    )

    passwords = view_vault(
        key
    )

    table = QTableWidget()

    table.setColumnCount(
        3
    )

    table.setHorizontalHeaderLabels(
        [
            "Website",
            "Username",
            "Password"
        ]
    )

    table.setRowCount(
        len(passwords)
    )

    for row, entry in enumerate(passwords):

        table.setItem(
            row,
            0,
            QTableWidgetItem(
                entry["website"]
            )
        )

        table.setItem(
            row,
            1,
            QTableWidgetItem(
                entry["username"]
            )
        )

        table.setItem(
            row,
            2,
            QTableWidgetItem(
                "********"
            )
        )

    table.resizeColumnsToContents()

    window.layout.addWidget(
        table
    )

    buttons = QHBoxLayout()

    edit_button = QPushButton(
        "Edit"
    )

    edit_button.setIcon(
        QIcon(
            icon_path("edit.svg")
        )
    )

    edit_button.clicked.connect(
        edit_password
    )

    delete_button = QPushButton(
        "Delete"
    )

    delete_button.setIcon(
        QIcon(
            icon_path("delete.svg")
        )
    )

    delete_button.clicked.connect(
        delete_password_gui
    )

    show_button = QPushButton(
        "Show"
    )

    show_button.clicked.connect(
        show_password
    )

    copy_button = QPushButton(
        "Copy"
    )

    copy_button.setIcon(
        QIcon(
            icon_path("copy.svg")
        )
    )

    copy_button.clicked.connect(
        copy_password
    )

    back = QPushButton(
        "Back"
    )

    back.clicked.connect(
        show_menu
    )

    buttons.addWidget(
        edit_button
    )

    buttons.addWidget(
        delete_button
    )

    buttons.addWidget(
        show_button
    )

    buttons.addWidget(
        copy_button
    )

    buttons.addWidget(
        back
    )

    window.layout.addLayout(
        buttons
    )


# =========================
# SHOW / HIDE PASSWORD
# =========================

def show_password():

    global showing_password

    row = table.currentRow()

    if row < 0:
        return

    if showing_password:

        table.setItem(
            row,
            2,
            QTableWidgetItem(
                "********"
            )
        )

        showing_password = False

    else:

        table.setItem(
            row,
            2,
            QTableWidgetItem(
                passwords[row]["password"]
            )
        )

        showing_password = True


# =========================
# COPY PASSWORD
# =========================

def copy_password():

    row = table.currentRow()

    if row < 0:
        return

    password = passwords[row]["password"]

    QApplication.clipboard().setText(
        password
    )

    QMessageBox.information(
        window,
        "Copied",
        "Password copied"
    )


# =========================
# DELETE PASSWORD
# =========================

def delete_password_gui():

    row = table.currentRow()

    if row < 0:
        return

    answer = QMessageBox.question(
        window,
        "Confirm",
        "Delete this password?"
    )

    if answer != QMessageBox.Yes:
        return

    with open(
        "vault.json",
        "r"
    ) as file:

        vault = json.load(file)

    vault.pop(row)

    with open(
        "vault.json",
        "w"
    ) as file:

        json.dump(
            vault,
            file,
            indent=4
        )

    view_passwords()


# =========================
# EDIT PASSWORD
# =========================

def edit_password():

    row = table.currentRow()

    if row < 0:
        return

    clear_screen()

    website = QLineEdit()

    website.setText(
        passwords[row]["website"]
    )

    username = QLineEdit()

    username.setText(
        passwords[row]["username"]
    )

    password = QLineEdit()

    password.setText(
        passwords[row]["password"]
    )

    window.layout.addWidget(
        website
    )

    window.layout.addWidget(
        username
    )

    window.layout.addWidget(
        password
    )

    save = QPushButton(
        "Save Changes"
    )

    def save_edit():

        encrypted = encrypt_data(
            password.text(),
            key
        )

        with open(
            "vault.json",
            "r"
        ) as file:

            vault = json.load(file)

        vault[row] = {

            "website": website.text(),

            "username": username.text(),

            "password": encrypted

        }

        with open(
            "vault.json",
            "w"
        ) as file:

            json.dump(
                vault,
                file,
                indent=4
            )

        view_passwords()

    save.clicked.connect(
        save_edit
    )

    window.layout.addWidget(
        save
    )
