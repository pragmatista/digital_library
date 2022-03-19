import os
import data.db_session as db_session
import workflow

from file_system.file_system_object import FileSystemObject
import subprocess
import file_system


def main():
    # path = '/Users/kyleking/Projects/_Admin/_Data/folder_hierarchy'
    # # path = 'test1.pdf'
    # include = []
    # exclude = ['.map', 'venv', '.pyc', '__pycache__', '.DS_Store', 'ignore', '.idea', 'git']
    # file_system.search(path, recursive=True, restricted_list=include, exclusion_list=exclude)
    # # search(path, recursive=True, restricted_list=include, exclusion_list=exclude)

    setup_db()
    workflow.main_menu()

#
# def search(search_path, recursive=True, restricted_list: list = None, exclusion_list: list = None):
#     fso = FileSystemObject(search_path)
#     results = []
#
#     if fso.file and not fso.is_hidden:  # file is specified as a full path
#         print("Single File", fso.to_dict())
#
#     elif fso.folder and recursive:
#         for root, folders, files in os.walk(search_path, topdown=True):
#             for folder in folders:
#                 fso = FileSystemObject(os.path.join(root, folder))
#                 if (
#                     not fso.is_hidden
#                     and fso.folder
#                     and include_in_search(fso.full_path, restricted_list=restricted_list, exclusion_list=exclusion_list)
#                 ):
#                     results.append(fso.to_dict())
#             for file in files:
#                 fso = FileSystemObject(os.path.join(root, file))
#                 if (
#                     not fso.is_hidden
#                     and fso.file
#                     and include_in_search(fso.full_path, restricted_list=restricted_list, exclusion_list=exclusion_list)
#                 ):
#                     results.append(fso.to_dict())
#
#     elif not recursive:
#         print("Single Folder", fso.to_dict())
#         for root, folders, files in os.walk(search_path):
#             for file in files:
#                 fso = FileSystemObject(os.path.join(root, file))
#                 if (
#                     not fso.is_hidden
#                     and fso.file
#                     and include_in_search(fso.full_path, restricted_list=restricted_list, exclusion_list=exclusion_list)
#                 ):
#                     results.append(fso.to_dict())
#             break
#
#     else:  # search is likely a partial name/wildcard search
#         search_folder = input("what directory would you like to search? ")
#         wildcard_search = '*' + search_path.lower() + '*'
#         cmd = ["find", search_folder, "-iname", wildcard_search]
#
#         matches = subprocess.run(cmd, text=True, stdout=subprocess.PIPE).stdout.splitlines()
#         for item in matches:
#             fso = FileSystemObject(item)
#             if include_in_search(fso.full_path, restricted_list, exclusion_list):
#                 results.append(fso.to_dict())
#
#     for item in results:
#         print(item)
#
#
# def include_in_search(path, restricted_list: list = None, exclusion_list: list = None):
#     if exclusion_list and any(path.lower().find(criteria.lower()) >= 0 for criteria in exclusion_list):
#         return False
#
#     if restricted_list and any(path.lower().find(criteria.lower()) >= 0 for criteria in restricted_list):
#         return True
#
#     return not restricted_list




def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'data/db', 'digital_library.db')
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()



