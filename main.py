from password_generator import runner , get_length, get_amount , ask_question , character_pool, generate_password, calculate_entropy , strength_checker
from vault import save_data
from authentication import login_screen , change_master_password
from vault import view_vault, search_vault, edit_vault, delete_password
from encryption import create_key

def main():
    while True:
         logged_in, master_password = login_screen()
         if logged_in :
                print("Vault unlocked")

                key = create_key(master_password)

                while True :
                    print("PASSWORD MANAGER")
                    print("1 generate")
                    print("2 view vault")
                    print("3 search vault")
                    print("4 edit vault")
                    print("5 delete password")
                    print("6 lock")
                    print("7 change master password")
                    print("8 exit")
                    choice = input("choose : ")

                    if choice == "1" :
                        runner(key)

                    elif choice == "2" :
                        view_vault(key)

                    elif choice == "3" :
                        search_vault(key)

                    elif choice == "4" :
                        edit_vault(key)

                    elif choice == "5" :
                        delete_password(key)

                    elif choice == "6" :
                        print("Vault locked")
                        break

                    elif choice == "7" :
                        change_master_password()

                    elif choice == "8" :
                        print("Goodbye")
                        return

                    else :
                        print("Invalid choice")

         else :
                print("Closing Program")


main()










