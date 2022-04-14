import services.inventory
import workflow
import file_system.upload
from services import library
import os
import face_recognition as fr
import cv2
import numpy as np

MODEL_BASE_PATH = ''
KNOWN_NAMES = []
KNOWN_NAME_ENCODINGS = []


def menu():
    global MODEL_BASE_PATH

    while True:
        cv2.destroyAllWindows()

        print("\n")
        print("###############################################")
        print("Digital Library Utility - Facial Recognition ")
        print("###############################################")
        print("[0] Return to Main Menu")
        print("[1] Manage Inventory")
        print("[2] Run Model")

        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(10):
            if int(choice) == 0:
                workflow.main_menu()

            elif int(choice) == 1:  # manage model inventory
                workflow.workflow_library.display_model_libraries()
                library_id = input("Select Library ID: ")

                lib = library.get_library(library_id)
                MODEL_BASE_PATH = lib.base_path
                print(MODEL_BASE_PATH)

                workflow.workflow_facial_recognition.model_inventory_workflow(lib.library_id)

            elif int(choice) == 2:  # run model
                test_mode = input("Run in test mode (Y/N): ")
                test_mode = test_mode.strip().upper() == "Y"

                model_lib = workflow.workflow_library.get_model_training_library()
                model_inv = workflow.workflow_inventory.get_inventory(library_id=model_lib.library_id)
                assignment = input("Filter on Model Assignment (Leave blank to ignore): ")
                filtered = [item for item in model_inv if item['model_assignment'] == assignment]
                model_inv = filtered or model_inv

                if test_mode:  # determine which library/inventory needs to be selected
                    data_lib = workflow.workflow_library.get_model_testing_library()
                else:
                    workflow.workflow_library.display_user_libraries()
                    library_id = input("Select Library ID: ")
                    data_lib = library.get_library(library_id)

                data_inv = workflow.workflow_inventory.get_inventory(library_id=data_lib.library_id)

                run_model(data_lib, data_inv, model_lib, model_inv, test_mode)

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
            workflow.workflow_facial_recognition.menu()

        elif int(choice) == 1:
            upload_images()
            workflow.workflow_inventory.refresh_inventory(library_id=library_id)

        elif int(choice) == 2:
            if services.inventory.get_library_inventory(library_id):
                workflow.workflow_inventory.update_classification(library_id=library_id, incl_assignment=True)

        elif int(choice) == 3:
            if services.inventory.get_library_inventory(library_id):
                workflow.workflow_inventory.display_library_inventory(library_id=library_id)
                remove_image()


def upload_images():
    print("\n")
    print("Specify the source location: ")
    src_path = input("> ")

    file_system.upload.upload_files(src=src_path, dest=MODEL_BASE_PATH, save_option=3)


def remove_image():
    inventory_id = workflow.workflow_inventory.select_inventory_item()
    inv = services.inventory.get_inventory_item(inventory_id)
    path = inv.full_path
    os.remove(path)
    services.inventory.delete_inventory_item(inventory_id)


def run_model(data_lib: library, data_inv: dict, model_lib: library, model_inv: dict, test_mode: bool = False):
    known_face_names = []
    known_face_encodings = []

    for file in model_inv:
        image = fr.load_image_file(file['full_path'])
        encoding = fr.face_encodings(image)[0]
        known_face_names.append(file['model_assignment'])
        known_face_encodings.append(encoding)

    for sample in data_inv:
        inventory_id = sample['inventory_id']
        test_image = sample['full_path']
        image = cv2.imread(test_image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            name = ""

            face_distances = fr.face_distance(known_face_encodings, face_encoding)
            best_match = np.argmin(face_distances)
            # print(f"Distances: {face_distances}")

            if matches[best_match]:
                name = known_face_names[best_match]
                workflow.workflow_inventory.update_classification_from_model(inventory_id=inventory_id, tags=name)

            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 3)
            cv2.rectangle(image, (left, bottom - 50), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom), font, 2.0, (255, 255, 255), 5)

            if test_mode:
                # cv2.imshow(sample['file'], image)
                cv2.imwrite(f"{data_lib.base_path}/output/{sample['file']}", image)
                # cv2.waitKey(100)
                # pause = input("Press Enter to Continue ")
                cv2.destroyAllWindows()
