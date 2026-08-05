from password_generator import runner , get_length, get_amount , ask_question , character_pool, generate_password, calculate_entropy , strength_checker
from vault import save_data
from authentication import   change_master_password
from vault import view_vault, search_vault, edit_vault, delete_password
from encryption import create_key
from gui import login_screen
from gui_pyside import startapp


def main():
    startapp()

if __name__ == "__main__":
    main()










