import services.inventory
import workflow
import file_system.upload
from services import library
import os

MODEL_TRAIN_PATH = ''


def model_menu():
    global MODEL_TRAIN_PATH
    lib = library.get_model_library()
    MODEL_TRAIN_PATH = lib.base_path
    print(MODEL_TRAIN_PATH)

    while True:
        print("\n")
        print("###############################################")
        print("Digital Library Utility - Training Model ")
        print("###############################################")
        print("[1] Manage Model Inventory")
        print("[2] Test Model")
        print("[3] Run/Apply Model on Inventory")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(10):
            if int(choice) == 0:
                workflow.main_menu()

            elif int(choice) == 1:  # manage model inventory
                workflow.workflow_model.model_inventory_workflow(lib.library_id)

            elif int(choice) == 2:  # test model
                workflow.workflow_inventory.display_library_inventory(library_id=lib.library_id)

            elif int(choice) == 3:  # apply model
                print("coming soon!")

        else:
            print("Selection not valid. Please try again.")


def model_inventory_workflow(library_id):
    print("[0] Return to Model Inventory Main Menu")
    print("[1] Add/Upload image to inventory")
    print("[2] Classify image for model")
    print("[3] Remove image from inventory")

    choice = input("> ")

    if choice.isnumeric() and int(choice) in range(4):
        if int(choice) == 0:
            workflow.workflow_model.model_menu()

        elif int(choice) == 1:
            upload_images()
            workflow.workflow_inventory.refresh_inventory(library_id=library_id)

        elif int(choice) == 2:
            if services.inventory.get_library_inventory(library_id):
                workflow.workflow_inventory.display_library_inventory(library_id=library_id)
                inventory_id = workflow.workflow_inventory.select_inventory_item()
                workflow.workflow_inventory.update_classification(inventory_id=inventory_id)

        elif int(choice) == 3:
            if services.inventory.get_library_inventory(library_id):
                workflow.workflow_inventory.display_library_inventory(library_id=library_id)
                inventory_id = workflow.workflow_inventory.select_inventory_item()
                remove_image(inventory_id)


def upload_images():
    print("\n")
    print("Specify the source location:")
    src_path = input("> ")

    file_system.upload.upload_files(src=src_path, dest=MODEL_TRAIN_PATH, save_option=3)


def remove_image(inventory_id):
    inv = services.inventory.get_inventory_item(inventory_id)
    path = inv.full_path
    os.remove(path)
    services.inventory.delete_inventory_item(inventory_id)
