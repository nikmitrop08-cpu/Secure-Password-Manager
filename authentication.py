import bcrypt
import json
import os
from encryption import create_key , encrypt_data, decrypt_data

CONFIG_FILE = "config.json"

def create_master_password() :

    master_password = input("Enter master password: ")



    salt =  bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(master_password.encode(), salt)

    data = {"password_hash" : hashed_password.decode() }

    with open(CONFIG_FILE, "w") as json_file:
        json.dump(data, json_file, indent = 4)

    print("Master password created")

def verify_user(password):



    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)

    stored_hash = data["password_hash"].encode()

    if bcrypt.checkpw(password.encode(), stored_hash) :
        return True

    return False

def master_password_exists():
    return os.path.exists(CONFIG_FILE)

def change_master_password(old_password , new_password):

    if verify_user(old_password) :

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        config["password_hash"] = new_hash.decode()

        with open(CONFIG_FILE, "w") as json_file:
            json.dump(config, json_file, indent = 4)

        return True

    return False
