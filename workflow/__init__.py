__all__ = ['workflow_library', 'workflow_inventory', 'workflow_tools', 'workflow_model']

# from workflow import workflow_library
import workflow.workflow_library
import workflow.workflow_inventory
import workflow.workflow_model
import workflow.workflow_tools
import pandas as pd
import file_system
from tabulate import tabulate


def main_menu():
    print("\n")
    print("#############################################")
    print("            Digital Library Utility          ")
    print("#############################################")
    print("[1] Library Management")
    print("[2] Inventory Management")
    print("[3] Model Inventory Management")
    print("[4] Tools")
    print("[X] Exit")
    choice = input("> ")

    if choice.isnumeric() and int(choice) in range(1, 5):
        if int(choice) == 1:
            workflow.workflow_library.library_menu()
        elif int(choice) == 2:
            workflow.workflow_inventory.inventory_menu()
        elif int(choice) == 3:
            workflow.workflow_model.model_menu()
        elif int(choice) == 4:
            workflow.workflow_tools.tools_menu()
    elif choice.isalpha() and choice.lower() == 'x':
        print("Goodbye!")
        exit()
    else:
        print("Selection not valid. Please try again.")
        main_menu()


def display_results(data):
    df = pd.DataFrame(data)
    print(tabulate(df, headers='keys', tablefmt='psql'))


def upload_files():
    print("\n")
    print("Specify the source path:")
    src_path = input("> ")

    print("Specify the destination path:")
    dest_path = input("> ")

    file_system.upload.upload_files(src=src_path, dest=dest_path)
