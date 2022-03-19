import datetime
import workflow
import pandas as pd
import numpy as np
import file_system
import file_system.images as images
from file_system.file_system_object import FileSystemObject
from services import inventory, library
from tabulate import tabulate


def inventory_menu():
    while True:
        print("\n")
        print("###############################################")
        print("Digital Library Utility - Inventory Management ")
        print("###############################################")
        print("[1] Add/Update (Refresh) Inventory")
        print("[2] View All Inventory")
        print("[3] View Inventory by Library")
        print("[4] Reconcile (Library) Inventory")
        print("[5] Update Inventory Compare Scores")
        print("[6] Manage Duplicate Inventory")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(7):
            if int(choice) == 0:
                workflow.main_menu()
            elif int(choice) == 1:  # add/update (refresh) inventory
                refresh_inventory()
            elif int(choice) == 2:  # view all inventory
                display_all_inventory()
            elif int(choice) == 3:  # view inventory by library
                display_library_inventory()
            elif int(choice) == 4:  # reconcile inventory
                reconcile_inventory(calculate_compare_score=False)
            elif int(choice) == 5:  # reconcile inventory
                reconcile_inventory(calculate_compare_score=True)
            elif int(choice) == 6:  # manage duplicate inventory
                find_duplicates()
        else:
            print("Selection not valid. Please try again.")


def refresh_inventory():
    library_id = prompt_for_library()
    src = get_library_base_path(library_id)
    exclusion_list = ['.map', 'venv', '.pyc', '__pycache__', '.DS_Store', 'ignore', '.idea', 'git']
    restricted_list = []

    data = file_system.search(search_path=src,
                              recursive=True,
                              exclusion_list=exclusion_list,
                              restricted_list=restricted_list)

    for idx, item in enumerate(data):
        data[idx]['library_id'] = library_id
        if not data[idx]['is_hidden']:
            inventory.refresh_inventory(**data[idx])
    return


def prompt_for_library():
    workflow.workflow_library.display_libraries()
    return input("Select Library ID: ")


def get_library_base_path(library_id):
    lib = library.get_library(library_id)
    return lib.base_path


def update_inventory_compare_scores(inventory_id, full_path):
    fso = FileSystemObject(full_path).to_dict()
    if fso and fso['is_found'] and not fso['is_hidden']:
        fso['inventory_removed_date'] = None
        inv = inventory.get_inventory_item(inventory_id)

        if not inv.compare_score or inv.compare_score == 0 or inv.compare_score_dt < inv.modified_dt:
            fso['compare_score'] = (update_compare_score(full_path, size=fso['size']))
            fso['compare_score_dt'] = datetime.datetime.now()

        inventory.update_inventory(inventory_id, **fso)
    else:
        data = {'inventory_removed_date': datetime.datetime.now()}
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
    library_id = prompt_for_library()

    results = inventory.get_library_inventory(library_id)
    df = pd.DataFrame(results)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.sort_values(by=['library_id', 'directory', 'full_path'])
    print(tabulate(df.head(500), headers='keys', tablefmt='psql'))


def reconcile_inventory(calculate_compare_score: bool = False):
    # Purpose: Identify files/folders that no longer exist and update DB accordingly
    library_id = prompt_for_library()
    results = inventory.get_library_inventory(library_id)

    for idx, item in enumerate(results):
        if results[idx]['file']:
            src_path = results[idx]['full_path']
            inventory_id = results[idx]['inventory_id']

            fso = FileSystemObject(src_path).to_dict()
            if fso and fso['is_found'] and not fso['is_hidden']:
                data = {'inventory_removed_date': None}
            else:
                data = {'inventory_removed_date': datetime.datetime.now()}

            inventory.update_inventory(inventory_id, **data)

            if calculate_compare_score:
                update_inventory_compare_scores(inventory_id, src_path)


def display_duplicates():
    pass


def find_duplicates():
    primary_id = None
    primary_image_array = None
    secondary_id = None
    secondary_image_array = None

    library_id = prompt_for_library()
    data = inventory.get_comparable_inventory(library_id)

    df = pd.DataFrame(data)
    df = df.drop(['_sa_instance_state'], axis=1)
    df["file"] = df["file"].str.lower()
    df['compare_score_frequency'] = df.groupby('compare_score')['compare_score'].transform('count')
    df = df[df.groupby('compare_score')['compare_score'].transform('count') > 1]
    df = df[['inventory_id', 'library_id', 'directory', 'full_path', 'file',
             'size', 'created_dt', 'modified_dt',
             'compare_score_dt', 'compare_score', 'compare_score_frequency']]
    # df.sort_values(by=['compare_score', 'size'])
    print(tabulate(df, headers='keys', tablefmt='psql'))

    distinct_scores = list(df['compare_score'].unique())
    count = len(distinct_scores)

    for counter, score in enumerate(distinct_scores, 1):
        sample = df[df["compare_score"] == score]
        sample = pd.DataFrame(sample, columns=['inventory_id', 'full_path'])
        sample.reset_index(drop=True, inplace=True)
        print("###############################################")
        print(f"Potential Duplicate Group {counter} of {count}")
        print("###############################################")
        print(tabulate(sample.head(100), headers='keys', tablefmt='psql'))


def add_duplicate(inventory_id, duplicate_of):
    print(f"{inventory_id} is a duplicate of: {duplicate_of}")

#
# def remove_duplicate_inventory(dest_path: str):
#     data = services.read.get_all_duplicates()
#     df = pd.DataFrame(data)
#     print(tabulate(df.head(100), headers='keys', tablefmt='psql'))
#
#     inventory_id = input("Please provide media library id: ")
#     parent_id = services.read.get_duplicate_id_from_media_id(media_id)
#
#     parent = services.read.get_file_details(parent_id)
#     parent_df = pd.DataFrame(parent)
#     print(tabulate(parent_df, headers='keys', tablefmt='psql'))
#     parent_src = parent_df['full_path'].to_list()[0]
#     parent_dest = str(dest_path + '/' + parent_df['media_id'].to_list()[0] + parent_df['extension'].to_list()[0])
#
#     duplicate = services.read.get_file_details(inventory_id)
#     duplicate_df = pd.DataFrame(duplicate)
#     print(tabulate(duplicate_df, headers='keys', tablefmt='psql'))
#     duplicate_src = parent_df['full_path'].to_list()[0]
#     duplicate_dest = str(
#         dest_path + '/' + duplicate_df['media_id'].to_list()[0] + duplicate_df['extension'].to_list()[0])
#
#     print(f"{parent_src}\n {parent_dest}")
#
#     # + '/' + duplicate_df['media_id'] + duplicate_df['extension'])
#
#     shutil.copy(parent_src, parent_dest)
#     shutil.copy(duplicate_src, duplicate_dest)
