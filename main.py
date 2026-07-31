from password_generator import get_length, get_amount , ask_question , character_pool, generate_password, calculate_entropy , strength_checker
from vault import save_data

def main():
    print ("Password Generator")

    length = get_length()

    amount = get_amount()

    uppercase = ask_question("Include uppercase?: ")
    lowercase = ask_question("Include lowercase?: ")
    digits = ask_question("Include digits?: ")
    symbols = ask_question("Include symbols?: ")

    characters = character_pool(uppercase, lowercase, digits, symbols)


    if characters == "" :
        print ("You must select at least one character type")
        return

    if length < sum ([uppercase, lowercase, digits, symbols]) :
        print("Password length is too short")
        return

    for i in range(amount):

        password = generate_password(length, characters, uppercase, digits, symbols, lowercase)

        entropy = calculate_entropy(password, characters)

        print("Generated password: ")
        print (password)
        print (f"Your password is {strength_checker(password, uppercase, lowercase, digits, symbols)}" )
        print("Entropy is", round(entropy, 2), "bits")

        save = input("Do you want to save this password? (y/n): ")

        if save == "y" :

            website = input("Enter website: ")
            username = input("Enter username: ")

            save_data(website, username, password)

            print("Your password has been saved")
        else :
            print("Your password is not saved")
main()