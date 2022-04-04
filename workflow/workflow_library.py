import services.library
import workflow
import pandas as pd
from services import library
from tabulate import tabulate


def library_menu():
    while True:
        print("\n")
        print("#############################################")
        print("Digital Library Utility - Library Management ")
        print("#############################################")
        print("[1] Add Library")
        print("[2] Update Library")
        print("[3] Remove Library")
        print("[4] View Libraries")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(5):
            if int(choice) == 0:
                workflow.main_menu()
            elif int(choice) == 1:  # add library
                add_library()
            elif int(choice) == 2:  # update library
                update_library()
            elif int(choice) == 3:  # remove library
                remove_library()
            elif int(choice) == 4:  # view libraries
                display_libraries()
        else:
            print("Selection not valid. Please try again.")


def add_library():
    data = {
        'library_name': input("Library Name: "),
        'description':  input("Description: "),
        'base_path':  input("Base Path: ")
    }

    library.add_library(**data)


def update_library():
    display_user_libraries()
    library_id = input("Provide the Library ID you wish to update: ")
    lib = services.library.get_library(library_id)

    if lib.library_id:
        print("Please provide the following information:")
        data = {
            'library_id': lib.library_id,
            'library_name': input("Library Name: (Leave blank for no change) "),
            'description': input("Description: (Leave blank for no change) "),
            'base_path': input("Base Path: (Leave blank for no change) ")
        }
        library.update_library(**data)
    else:
        print("Library ID was not valid")
        update_library()


def remove_library():
    display_user_libraries()
    library_id = input("Provide the Library ID you wish to remove: ")
    lib = services.library.get_library(library_id)
    if lib.library_id:
        services.library.remove_library(lib.library_id)
    else:
        print("Library ID was not valid")
        remove_library()


def display_user_libraries():
    try:
        data = library.get_user_libraries()
        df = pd.DataFrame(data)
        # df = df.drop(['_sa_instance_state'], axis=1)
        df = df[['library_id', 'library_name', 'description', 'base_path', 'created_date', 'modified_date', 'removed_date']]
        print(tabulate(df.head(500), headers='keys', tablefmt='psql'))
    except KeyError:
        print("No Libraries Currently Exist")


def display_libraries():
    try:
        data = library.get_all_libraries()
        df = pd.DataFrame(data)
        # df = df.drop(['_sa_instance_state'], axis=1)
        df = df[['library_id', 'library_name', 'description', 'base_path', 'created_date', 'modified_date', 'removed_date']]
        print(tabulate(df.head(500), headers='keys', tablefmt='psql'))
    except KeyError:
        print("No Libraries Currently Exist")

