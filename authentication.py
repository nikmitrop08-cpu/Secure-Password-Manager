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

def change_master_password():

    logged_in, old_password = verify_user()

    if logged_in :

        old_key = create_key(old_password)

        with open("vault.json" , "r") as file :
            vault = json.load(file)

        decrypted_vault = []

        for item in vault:
            password = decrypt_data(item["password"], old_key)

            decrypted_vault.append({"website": item["website"], "username": item ["username"],"password": password})

        new_password = input("new master password: ")

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

        with open("config.json" , "r") as file:
            config = json.load(file)

        config["password_hash"] = new_hash.decode()

        with open("config.json", "w") as file :
            json.dump(config, file, indent=4)

        new_key = create_key(new_password)

        encrypted_vault = []

        for item in decrypted_vault:

            encrypted_password = encrypt_data(item["password"], new_key)

            encrypted_vault.append({"website": item["website"], "username": item["username"],"password": encrypted_password.decode()})

        with open("vault.json", "w") as file:
            json.dump(encrypted_vault, file, indent = 4)

        print("Master password changed")

    else:
        print("Wrong password")

