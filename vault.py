import json

VAULT_FILE = "vault.json"

def save_data(website, username, password ) :

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

    vault.append(entry)

    with open (VAULT_FILE, "w") as file :
        json.dump(vault, file, indent = 4)

    print("Password saved")

def view_vault() :
    try :
        with open(VAULT_FILE, "r") as file :
            vault = json.load(file)

        if not vault         :
            print("vault is empty")
            return

        print("SAVED PASSWORDS")

        for entry in vault:

            print("-----------------")
            print("Website:", entry["website"])
            print("Username:", entry["username"])
            print("password:", entry["password"])

    except FileNotFoundError :
        print("vault does not exist")

def search_vault():

    search = input("search website: ").lower()

    try:

        with open(VAULT_FILE, "r") as file:

            vault = json.load(file)

        found = False

        for entry in vault :

            if search in entry["website"].lower():
                print("-----------------")
                print("Website:", entry["website"])
                print("Username:", entry["username"])
                print("Password:",entry["password"])

                found = True

            if not found:
                print("Password not found")

    except FileNotFoundError :
        print("Vault file does not exist")


