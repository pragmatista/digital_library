import datetime
import shutil
import services.inventory
import workflow
import pandas as pd
import os
import file_system
import file_system.images as images
from file_system.file_system_object import FileSystemObject
from services import inventory, library
from tabulate import tabulate

TEMP_FOLDER = "tmp/eval"
RECYCLE_BIN = "tmp/recycle_bin"


def inventory_menu():
    library_id = prompt_for_library()

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
        print("[7] Restore files from Recycle Bin")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(8):
            if int(choice) == 0:
                workflow.main_menu()

            elif int(choice) == 1:  # add/update inventory
                refresh_inventory(library_id=library_id)
                reconcile_inventory(library_id=library_id, calculate_compare_score=False)

            elif int(choice) == 2:  # view all inventory
                display_all_inventory()

            elif int(choice) == 3:  # view inventory by library
                display_library_inventory(library_id)

            elif int(choice) == 4:  # reconcile inventory
                reconcile_inventory(library_id=library_id, calculate_compare_score=False)

            elif int(choice) == 5:  # reconcile inventory with compare score calculation
                reconcile_inventory(library_id=library_id, calculate_compare_score=True)

            elif int(choice) == 6:  # manage duplicate inventory
                refresh_inventory(library_id=library_id)
                reconcile_inventory(library_id=library_id, calculate_compare_score=True)
                get_comparable_inventory(library_id=library_id)
                move_files_to_recycle_bin(library_id=library_id)
                clear_eval_folder(TEMP_FOLDER)
                refresh_inventory(library_id=library_id)

            elif int(choice) == 7:
                restore_from_recycle_bin()
                reconcile_inventory(library_id=library_id, calculate_compare_score=False)

        else:
            print("Selection not valid. Please try again.")


def refresh_inventory(library_id):
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


def display_library_inventory(library_id):
    results = inventory.get_library_inventory(library_id)
    df = pd.DataFrame(results)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.sort_values(by=['library_id', 'directory', 'full_path'])
    print(tabulate(df.head(500), headers='keys', tablefmt='psql'))


def reconcile_inventory(library_id, calculate_compare_score: bool = False):
    # Purpose: Identify files/folders that no longer exist and update DB accordingly
    # library_id = prompt_for_library()
    results = inventory.get_library_inventory(library_id)

    for idx, item in enumerate(results):
        if results[idx]['file']:
            src_path = results[idx]['full_path']
            inventory_id = results[idx]['inventory_id']

            fso = FileSystemObject(src_path).to_dict()
            if fso and fso['is_found'] and not fso['is_hidden']:
                data = {
                    'inventory_removed_date': None,
                    'inventory_removed_reason': None,
                    'is_missing': False
                        }
            else:
                data = {'inventory_removed_date': datetime.datetime.now(),
                        'is_missing': True
                        }

            inventory.update_inventory(inventory_id, **data)

            if calculate_compare_score:
                update_inventory_compare_scores(inventory_id, src_path)


def restore_from_recycle_bin():
    path = RECYCLE_BIN
    for root, folders, files in os.walk(path, topdown=True):
        for file in files:
            recycled_file = os.path.splitext(file)[0]
            src = os.path.join(root, file)
            original_file = services.inventory.get_inventory_item(recycled_file)
            dest = original_file.full_path

            shutil.move(src, dest)


def get_comparable_inventory(library_id):
    try:
        if data := inventory.get_comparable_inventory(library_id):
            df = pd.DataFrame(data)
            df = df.drop(['_sa_instance_state'], axis=1)
            df["file"] = df["file"].str.lower()
            df['compare_score_frequency'] = df.groupby('compare_score')['compare_score'].transform('count')
            df = df[df.groupby('compare_score')['compare_score'].transform('count') > 1]
            df = df[['inventory_id', 'library_id', 'directory', 'full_path', 'file', 'file_extension',
                     'size', 'created_dt', 'modified_dt',
                     'compare_score_dt', 'compare_score', 'compare_score_frequency']]
            # df.sort_values(by=['compare_score', 'size'])
            # print(tabulate(df, headers='keys', tablefmt='psql'))
            group_duplicates(df)
            clear_eval_folder(TEMP_FOLDER)
        else:
            print("No duplicates were found.")
    except:
        print("An unexpected error has occurred")


def group_duplicates(df: pd.DataFrame):
    distinct_scores = list(df['compare_score'].unique())
    count = len(distinct_scores)

    for counter, score in enumerate(distinct_scores, 1):
        sample = df[df["compare_score"] == score]
        sample = pd.DataFrame(sample, columns=['inventory_id', 'file', 'file_extension', 'full_path', 'directory',
                                               'size', 'created_dt', 'modified_dt'])
        sample.reset_index(drop=True, inplace=True)
        print("###############################################")
        print(f"Potential Duplicate Group {counter} of {count}")
        print(f"Compare Score: {score}")
        print("###############################################")

        evaluate_duplicates_by_group(sample)


def evaluate_duplicates_by_group(sample: pd.DataFrame):
    clear_eval_folder(path=TEMP_FOLDER)
    group = []
    # print(tabulate(sample.head(), headers='keys', tablefmt='psql'))

    for idx, row in sample.iterrows():
        group.append(row['inventory_id'])
        inventory_id = row['inventory_id']
        created = row['created_dt']
        modified = row['modified_dt']
        size = row['size']
        src = row['full_path']
        dest = f'{TEMP_FOLDER}/' + inventory_id + row['file_extension']
        print(f"InventoryID: {inventory_id} | File: {row['file']} | Created: {created} | "
              f"Modified: {modified} | Size: {size}")

        shutil.copy2(src, dest)

    if retain := input("Enter Inventory IDs you wish to keep (separate by comma): ").split(","):
        for idx, item in enumerate(retain):
            retain[idx] = item.strip()

        for inv_id in group:
            if inv_id not in retain:
                reason = input(f"Enter reason for removal of {inv_id}: ")
                services.inventory.remove_inventory_item(inv_id.strip(), reason.strip())


def move_files_to_recycle_bin(library_id):
    reconcile_inventory(library_id, calculate_compare_score=False)
    if data := inventory.get_removed_inventory(library_id):
        for idx, item in enumerate(data):
            src = data[idx]['full_path']
            inventory_id = data[idx]['inventory_id']
            file_extension = data[idx]['file_extension']
            dest = f'{RECYCLE_BIN}/' + inventory_id + file_extension

            try:
                shutil.move(src, dest)
            except FileNotFoundError:
                print("A FileNotFound error has occurred.")


def remove_inventory(group: list, retain: list):
    for idx, item in enumerate(retain):
        retain[idx] = item.strip()

    for inv_id in group:
        if inv_id not in retain:
            reason = input(f"Enter reason for removal of {inv_id}: ")
            services.inventory.remove_inventory_item(inv_id.strip(), reason.strip())


def clear_eval_folder(path: str):
    mypath = path
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
