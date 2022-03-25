__all__ = ['workflow_library', 'workflow_inventory', 'workflow_tools']

# from workflow import workflow_library
import workflow.workflow_library
import workflow.workflow_inventory
import workflow.workflow_tools
import pandas as pd
from tabulate import tabulate


def main_menu():
    print("\n")
    print("#############################################")
    print("            Digital Library Utility          ")
    print("#############################################")
    print("[1] Library Management")
    print("[2] Inventory Management")
    print("[3] Tools")
    print("[X] Exit")
    choice = input("> ")

    if choice.isnumeric() and int(choice) in range(1, 4):
        if int(choice) == 1:
            workflow.workflow_library.library_menu()
        elif int(choice) == 2:
            workflow.workflow_inventory.inventory_menu()
        elif int(choice) == 3:
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
