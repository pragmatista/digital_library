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
        print("[3] Extract Text from PDFs")
        print("[4] Search for Files")
        print("[5] Find Text w/in Documents")
        print("[6] Find Text w/in Images")
        print("[0] Return to Main Menu")
        choice = input("> ")

        if choice.isnumeric() and int(choice) in range(7):
            if int(choice) == 0:
                workflow.main_menu()
            elif int(choice) == 1:  # backup
                file_system.backup.backup()
            elif int(choice) == 2:  # extract text from images
                workflow.workflow_tools.extract_image_text()
            elif int(choice) == 3:  # extract text from PDFs
                workflow.workflow_tools.extract_pdf_text()
            elif int(choice) == 4:  # search for files
                workflow.workflow_tools.custom_file_search()
            elif int(choice) == 5:  # search for text w/in files
                workflow.workflow_tools.custom_text_search()
            elif int(choice) == 6:  # find text w/in image files
                workflow.workflow_tools.extract_image_text(keyword_search=True)
        else:
            print("Selection not valid. Please try again.")


def custom_text_search():
    text = input("Text to Search: ")
    path = input("Folder Path: ")
    results = file_system.find_text_in_files(text, path)
    workflow.display_results(results)


def custom_file_search():
    path = input("Directory to Search: ")
    required = input("Include files that match the following (use comma to separate values): ").split(',')
    exclusions = input("Exclude the following files or file types (use comma to separate values): ").split(',')

    restricted_list = [item.strip() for item in required if item]
    exclusion_list = [item.strip() for item in exclusions if item]

    files = file_system.search(path, restricted_list=restricted_list, exclusion_list=exclusion_list)
    workflow.display_results(files)

    # for idx, file in enumerate(files):
    #     print(files[idx])
    # return


def extract_image_text(keyword_search: bool = False):
    text = input("Text/Phrase to Search: ") if keyword_search else None
    path = input("Please provide the directory to search: ")
    results = []

    files = file_system.search(path)  # returns list of dictionaries representing each file as an FSO object

    for idx, file in enumerate(files):
        if not files[idx]['is_hidden'] and files[idx]['is_image']:
            file['extracted_text'] = file_system.images.extract_text_from_image(files[idx]['full_path'], text)
            results.append(file) if file['extracted_text'] else None

    workflow.display_results(results)


def extract_pdf_text():
    path = input("Please provide the directory to search: ")
    results = []

    files = file_system.search(path)

    for idx, file in enumerate(files):
        if not files[idx]['is_hidden'] and str(files[idx]['file_extension']).lower() == '.pdf':
            pdf_data = file_system.pdf.extract_text_from_pdf(files[idx]['full_path'])

            file['pdf_total_pages'] = pdf_data[0]['total_pages']
            file['pdf_extracted_text'] = pdf_data[0]['text']

            results.append(file) if file['pdf_extracted_text'] else None

    workflow.display_results(results)


