#vault
import json
from encryption import create_key, encrypt_data, decrypt_data

VAULT_FILE = "vault.json"

def save_data(website, username, password , key) :


    entry = {
        "website" : website,
        "username" : username,
        "password" : password,
    }

    try :
        with open(VAULT_FILE , "r") as file :
            vault = json.load(file)

    except FileNotFoundError :
        vault = []


    encrypted_password = encrypt_data(password, key)

    entry["password"] = encrypted_password

    vault.append(entry)

    with open (VAULT_FILE, "w") as file :
        json.dump(vault, file, indent = 4)

    print("Password saved")

def view_vault(key) :

    print("view vault started")
    try :
        with open(VAULT_FILE, "r") as file :
            vault = json.load(file)
            print("loaded", vault)

    except FileNotFoundError:
        print("vault does not exist")

    if not vault:
        print("vault is empty")
        return []
    decrypted_vault = []
    for entry in vault:
        print("ENTRY", entry)
        decrypted_entry= {
            "website" : entry["website"],
            "username" : entry["username"],
            "password" : decrypt_data(entry["password"], key)
        }
        decrypted_vault.append(decrypted_entry)

    return decrypted_vault

def search_vault(key):

    search = input("search website: ").lower()

    try:

        with open(VAULT_FILE, "r") as file:

            vault = json.load(file)

        found = False

        for entry in vault :

            if search in entry["website"].lower():
                print("VIEW KEY", key)
                encrypted_password = entry["password"]
                password = decrypt_data(encrypted_password, key)
                print("-----------------")
                print("Website:", entry["website"])
                print("Username:", entry["username"])
                print("Password:", password)

                found = True

            if not found:
                print("Password not found")

    except FileNotFoundError :
        print("Vault file does not exist")

def edit_vault(key):

    website = input("Enter website to edit: ").lower()

    try:
        with open(VAULT_FILE, "r") as file :

            vault = json.load(file)

        found = False

        for entry in vault :




            if   entry ["website"].lower() ==  website:

                print("EDIT PASSWORD")

                new_username = input("New username: ")
                new_password = input("New password: ")

                entry["username"] = new_username
                encrypted_password = encrypt_data(new_password.encode(), key)
                entry["password"] = encrypted_password.decode()

                found = True

        if found:

            with open(VAULT_FILE, "w") as file:

                json.dump(vault, file, indent=4)

            print("Password updated successfully.")

        else:
            print("Website not found")

    except FileNotFoundError :
        print("Vault does not exist")

def delete_password(key):

    website = input("Enter a website to delete: ")

    try:

        with open(VAULT_FILE, "r") as file :
            vault = json.load(file)

        found = False

        for entry in vault:

            if entry["website"].lower() == website :

                vault.remove(entry)

                found = True

                break

        if found :
                with open(VAULT_FILE , "w") as file:
                    json.dump(vault , file, indent=4)

                print("Password deleted successfully")

        else :
                print("Website not found")

    except FileNotFoundError:

        print("Vault does not exist")

