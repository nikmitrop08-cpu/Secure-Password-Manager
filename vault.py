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
