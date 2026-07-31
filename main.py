from password_generator import runner , get_length, get_amount , ask_question , character_pool, generate_password, calculate_entropy , strength_checker
from vault import save_data
from authentication import login_screen
from vault import view_vault, search_vault

def main():


    if login_screen():
        print("Vault unlocked")


    while True :
        print("PASSWORD MANAGER")
        print("1 generate")
        print("2 view vault")
        print("3 search vault")
        print("4 exit")

        choice = input("choose : ")

        if choice == "1" :
            runner()

        elif choice == "2" :
            view_vault()

        elif choice == "3" :
            search_vault()

        elif choice == "4" :
            print("Goodbye")
            break
        else :
            print("Invalid choice")

    else :
        print("Closing Program")


main()