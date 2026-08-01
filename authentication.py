import bcrypt
import json
import os

CONFIG_FILE = "config.json"

def create_master_password() :

    master_password = input("Enter master password: ")

    master_password = master_password.encode()

    salt =  bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(master_password, salt)

    data = {"password_hash" : hashed_password.decode() }

    with open(CONFIG_FILE, "w") as json_file:
        json.dump(data, json_file, indent = 4)

    print("Master password created")

def verify_user():

    master_password = input("Enter master password: ")

    master_password = master_password.encode()

    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)

    stored_hash = data["password_hash"].encode()

    if bcrypt.checkpw(master_password, stored_hash) :
        return True, master_password

    return False ,None

def master_password_exists():
    return os.path.exists(CONFIG_FILE)

def login_screen():

    if not master_password_exists() :
        print("no master password found")
        create_master_password()
        master_password = create_master_password()
        return True , master_password

    attempts = 3

    while attempts > 0 :
        print("Login")
        logged_in , master_password = verify_user()
        if logged_in :
            print("Login successful")

            return True , master_password

        else :
            attempts -= 1

            print(f"Wrong password . Attempts left : {attempts}")

    print("Access denied")
    return False , None