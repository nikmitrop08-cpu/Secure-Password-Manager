#how long / uppercase / include numbers / inlcude symbols
import random
import string


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

def generate_password(length,characters):
    password = ""
    for i in range(length):
        password += random.choice(characters)

    return password
def main():
    print ("Password Generator")

    length = get_length()
    uppercase = ask_question("Include uppercase?: ")
    lowercase = ask_question("Include lowercase?: ")
    digits = ask_question("Include digits?: ")
    symbols = ask_question("Include symbols?: ")

    characters = character_pool(uppercase, lowercase, digits, symbols)

    password = generate_password(length,characters)

    print (password)

main()