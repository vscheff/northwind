import os


# Used to retrieve user input for record fields
# param     prompt - String used to prompt user for input
# param allow_null - Whether to allow an empty field or not
def get_user_input(prompt: str, allow_null: bool = False):
    while True:
        usr_inp = input(prompt)
        if usr_inp:
            return usr_inp
        if allow_null:
            return None

        print("ERROR: NULL value not allowed for this field.")


# Clears the terminal screen
def clear_screen():
     os.system('cls' if os.name == 'nt' else 'clear')

