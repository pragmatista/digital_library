import datetime

import workflow
import pandas as pd
from file_system.search import Search
from file_system.file_system_object import FileSystemObject
import file_system.images as images
from services import inventory
from tabulate import tabulate


def inventory_menu():

    while True:
        print("\n")
        print("###############################################")
        print("Digital Library Utility - Inventory Management ")
        print("###############################################")
        print("[1] Add (Library) Inventory")
        print("[2] View All Inventory")
        print("[3] View Inventory by Library")
        print("[4] Reconcile (Library) Inventory")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(5):
            if int(choice) == 0:
                workflow.main_menu()
            elif int(choice) == 1:  # add inventory to library
                scan_directory()
            elif int(choice) == 2:  # view all inventory
                display_all_inventory()
            elif int(choice) == 3:  # view inventory by library
                display_library_inventory()
            elif int(choice) == 4:  # reconcile inventory
                reconcile_inventory()
        else:
            print("Selection not valid. Please try again.")


def scan_directory():
    workflow.workflow_library.display_libraries()
    library_id = input("Select Library ID: ")
    src = "/Users/kyleking/Projects/_Admin/_Data/folder_hierarchy"  # input("Select the directory to scan: ")

    search = Search(search_path=src,
                    recursive=True,
                    return_all=True,
                    ignore=['.map', 'venv', '.pyc', '__pycache__', '.DS_Store', 'ignore', '.idea', 'git'],
                    require=[])
    data = search.execute()

    for idx, item in enumerate(data['results']):
        data['results'][idx]['library_id'] = library_id
        if not data['results'][idx]['is_hidden']:
            inventory.refresh_inventory(**data['results'][idx])
    return


def refresh_item(inventory_id, full_path):
    fso = FileSystemObject(full_path).to_dict()
    if fso and fso['is_found'] and not fso['is_hidden']:

        fso['inventory_removed_date'] = None
        inv = inventory.get_inventory_item(inventory_id)

        if not inv.compare_score or inv.compare_score == 0 or inv.compare_score_dt < inv.modified_dt:
            fso['compare_score'] = (update_compare_score(full_path, size=fso['size']))
            fso['compare_score_dt'] = datetime.datetime.now()

        inventory.update_inventory(inventory_id, **fso)

    else:
        data = {
            'inventory_removed_date': datetime.datetime.now()
        }
        inventory.update_inventory(inventory_id, **data)


def update_compare_score(full_path, size):
    return images.calculate_compare_score(full_path, size=size)


def display_all_inventory():
    results = inventory.get_all_inventory()
    df = pd.DataFrame(results)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.sort_values(by=['library_id', 'directory', 'full_path'])
    print(tabulate(df.head(500), headers='keys', tablefmt='psql'))


def display_library_inventory():
    workflow.workflow_library.display_libraries()
    library_id = input("Select Library ID: ")
    results = inventory.get_library_inventory(library_id)
    df = pd.DataFrame(results)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.sort_values(by=['library_id', 'directory', 'full_path'])
    print(tabulate(df.head(500), headers='keys', tablefmt='psql'))


def reconcile_inventory():
    workflow.workflow_library.display_libraries()
    library_id = input("Select Library ID: ")
    results = inventory.get_library_inventory(library_id)

    for idx, item in enumerate(results):
        if results[idx]['file']:
            # print(results[idx]['full_path'])
            refresh_item(results[idx]['inventory_id'], results[idx]['full_path'])

    # return

