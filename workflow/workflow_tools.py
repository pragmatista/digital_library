import workflow
import file_system
import file_system.pdf


def tools_menu():
    while True:
        print("\n")
        print("#############################################")
        print("Digital Library Utility - Tools ")
        print("#############################################")
        print("[1] Backup Files")
        print("[2] Extract Text from Images")
        print("[3] Extract Text from PDF")
        print("[4] Search for Files")
        print("[5] Find Text w/in Files")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(5):
            if int(choice) == 0:
                workflow.main_menu()
            elif int(choice) == 1:  # backup
                file_system.backup.backup()
            elif int(choice) == 2:  # extract text from images
                workflow.workflow_tools.extract_image_text_prompt()
            elif int(choice) == 3:  # extract text from PDFs
                workflow.workflow_tools.extract_pdf_text_prompt()
            elif int(choice) == 4:  # search for files
                file_system.search()
            elif int(choice) == 5:  # search for text w/in files
                file_system.find_text_in_files()
        else:
            print("Selection not valid. Please try again.")


def custom_file_search():
    path = input("Directory to Search:")
    include = input("Include files that match the following (use comma to separate values): ")
    exclude = input("Exclude the following files or file types (use comma to separate values): ")


def extract_image_text_prompt():
    path = input("Please provide the directory to search: ")

    files = file_system.search(path)

    for idx, file in enumerate(files):
        if not files[idx]['is_hidden'] and files[idx]['is_image']:
            file_system.images.extract_text(files[idx]['full_path'])
    return


def extract_pdf_text_prompt():
    path = input("Please provide the directory to search: ")

    files = file_system.search(path)
    results = [
        file_system.pdf.extract_text(files[idx]['full_path'])
        for idx, file in enumerate(files)
        if not files[idx]['is_hidden']
        and str(files[idx]['file_extension']).lower() == '.pdf'
    ]

    for item in results:
        print(item)

    return
