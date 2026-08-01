#how long / uppercase / include numbers / inlcude symbols
import json
import secrets
import string
import math
from vault import save_data

def get_length():
    while True:
        length = input("Enter length of password: ")

        if length.isdigit() and int(length) > 0 :
            return int(length)
        else :
            print("enter a valid length")

def ask_question(question):
    while True:
        answer = input(question + " (Y/N): ")

        if answer in ["Y","y"]:
            return True
        if answer in ["N","n"]:
            return False

        print("enter a valid answer")

def character_pool(lowercase, uppercase, digits, symbols):
    characters = ""

    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if symbols:
        characters += string.punctuation
    return characters

def generate_password(length,characters, uppercase, digits, symbols, lowercase):


    password = ""

    if uppercase:
        password += secrets.choice(string.ascii_uppercase)

    if lowercase:
        password += secrets.choice(string.ascii_lowercase)

    if digits:
        password += secrets.choice(string.digits)

    if symbols:
        password += secrets.choice(string.punctuation)

    while len(password) < length:
        password += secrets.choice(characters)

    password_list = list(password)

    mixed_password = ""

    while password_list :
        character = secrets.choice(password_list)
        mixed_password += character
        password_list.remove(character)

    return mixed_password



def strength_checker(password, uppercase, lowercase, digits, symbols) :
    score = 0
    if len(password) >= 8 :
        score += 1
    if uppercase :
        score += 1
    if digits :
        score += 1
    if symbols :
        score += 1
    if score <=1 :
        return "Weak"
    if score <=3 :
        return "Medium"
    else :
        return "Strong"

def get_amount() :
    while True:
        amount = input("Enter amount of passwords: ")

        if amount.isdigit() and int(amount) > 0 :
            return int(amount)

        print("enter a valid amount")

def calculate_entropy(password, characters) :
    length = len(password)
    pool_size = len(characters)

    entropy = length * math.log2(pool_size)

    return entropy


def runner(key):
    length = get_length()

    amount = get_amount()

    uppercase = ask_question("Include uppercase?: ")
    lowercase = ask_question("Include lowercase?: ")
    digits = ask_question("Include digits?: ")
    symbols = ask_question("Include symbols?: ")

    characters = character_pool(uppercase, lowercase, digits, symbols)

    if characters == "":
        print("You must select at least one character type")
        return

    if length < sum([uppercase, lowercase, digits, symbols]):
        print("Password length is too short")
        return

    for i in range(amount):

        password = generate_password(length, characters, uppercase, digits, symbols, lowercase)

        entropy = calculate_entropy(password, characters)

        print("Generated password: ")
        print(password)
        print(f"Your password is {strength_checker(password, uppercase, lowercase, digits, symbols)}")
        print("Entropy is", round(entropy, 2), "bits")

        save = input("Do you want to save this password? (y/n): ")

        if save == "y":

            website = input("Enter website: ")
            username = input("Enter username: ")

            save_data(website, username, password,key )

            print("Your password has been saved")
        else:
            print("Your password is not saved")
    return password