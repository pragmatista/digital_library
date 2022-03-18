import workflow
from file_system import backup


def tools_menu():
    while True:
        print("\n")
        print("#############################################")
        print("Digital Library Utility - Tools ")
        print("#############################################")
        print("[1] Backup Files")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(5):
            if int(choice) == 0:
                workflow.main_menu()
            elif int(choice) == 1:  # backup
                backup.backup()

        else:
            print("Selection not valid. Please try again.")

