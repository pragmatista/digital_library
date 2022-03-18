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
                display_libraries()
                update_library()
            elif int(choice) == 3:  # remove library
                remove_library()
            elif int(choice) == 4:  # view libraries
                display_libraries()
        else:
            print("Selection not valid. Please try again.")


def collect_info(library_id: str = None):
    print("Please provide the following information:")
    if library_id:
        library_name = input("Library Name: (Leave blank for no change) ")
        description = input("Description: (Leave blank for no change) ")
        base_path = input("Base Path: (Leave blank for no change) ")
    else:
        library_name = input("Library Name: ")
        description = input("Description: ")
        base_path = input("Base Path: ")

    return {
        'library_id': library_id,
        'library_name': library_name,
        'description': description,
        'base_path': base_path
    }


def add_library():
    data = collect_info()
    library.add_library(**data)


def update_library():
    library_id = input("Provide the Library ID you wish to update: ")
    data = collect_info(library_id)
    library.update_library(**data)


def remove_library():
    pass


def display_libraries():
    try:
        data = library.get_all_libraries()
        df = pd.DataFrame(data)
        df = df.drop(['_sa_instance_state'], axis=1)
        df = df[['library_id', 'library_name', 'description', 'base_path', 'created_date', 'modified_date', 'removed_date']]
        print(tabulate(df.head(500), headers='keys', tablefmt='psql'))
    except KeyError:
        print("No Libraries Currently Exist")
