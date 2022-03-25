__all__ = ['file_system_object', 'backup', 'images', 'pdf']

import os
import subprocess
from file_system.file_system_object import FileSystemObject


def search(search_path, recursive=True, restricted_list: list = None, exclusion_list: list = None):
    fso = FileSystemObject(search_path)
    results = []

    if fso.file and not fso.is_hidden:  # file is specified as a full path
        results.append(fso.to_dict())

    elif fso.folder and recursive:
        folders = search_folders(search_path,
                       recursive=recursive,
                       restricted_list=restricted_list,
                       exclusion_list=exclusion_list)
        results.extend(iter(folders))
        files = search_files(search_path,
                     recursive=recursive,
                     restricted_list=restricted_list,
                     exclusion_list=exclusion_list)

        results.extend(iter(files))
    else:  # search is likely a partial name/wildcard search
        search_folder = input("what directory would you like to search? ")
        wildcard_search = f'*{search_path.lower()}*'
        cmd = ["find", search_folder, "-iname", wildcard_search]

        matches = subprocess.run(cmd, text=True, stdout=subprocess.PIPE).stdout.splitlines()
        for item in matches:
            fso = FileSystemObject(item)
            if include_in_search(fso.full_path, restricted_list, exclusion_list):
                results.append(fso.to_dict())

    return results


def search_folders(search_path, recursive=True,
                   restricted_list: list = None,
                   exclusion_list: list = None):

    results = []

    for root, folders, files in os.walk(search_path, topdown=True):
        for folder in folders:
            fso = FileSystemObject(os.path.join(root, folder))
            if (
                    not fso.is_hidden
                    and fso.folder
                    and include_in_search(fso.full_path, restricted_list=restricted_list, exclusion_list=exclusion_list)
            ):
                fso = calculate_folder(fso)
                results.append(fso.to_dict())

            if not recursive:
                break

    return results


def calculate_folder(fso: FileSystemObject):
    path = fso.full_path
    for root, folders, files in os.walk(path, topdown=True):
        for folder in folders:
            folder_path = os.path.join(root, folder)
            fso_folder = FileSystemObject(folder_path)
            if fso.folder:
                fso.folder_count += 1

        for file in files:
            file_path = os.path.join(root, file)
            fso_file = FileSystemObject(file_path)

            if fso_file.file and not fso_file.is_hidden:
                fso.file_count += 1
                fso.size += fso_file.size
                fso.size_kb += fso_file.size_kb
                fso.size_mb += fso_file.size_mb
                fso.size_gb += fso_file.size_gb

    return fso


def search_files(search_path, recursive=True,
                   restricted_list: list = None,
                   exclusion_list: list = None):

    results = []
    for root, folders, files in os.walk(search_path, topdown=True):
        for file in files:
            fso = FileSystemObject(os.path.join(root, file))
            if (
                    not fso.is_hidden
                    and fso.file
                    and include_in_search(fso.full_path, restricted_list=restricted_list, exclusion_list=exclusion_list)
            ):
                results.append(fso.to_dict())
            if not recursive:
                break

    return results


def include_in_search(path, restricted_list: list = None, exclusion_list: list = None):
    if exclusion_list and any(path.lower().find(criteria.lower()) >= 0 for criteria in exclusion_list):
        return False
    if restricted_list and any(path.lower().find(criteria.lower()) >= 0 for criteria in restricted_list):
        return True

    return not restricted_list


def find_text_in_files(text, path):
    cmd = ['grep', '-irne', text, path]
    results = subprocess.run(cmd, text=True, stdout=subprocess.PIPE).stdout.splitlines()
    output = []
    for result in results:
        file = list(result.split(":"))
        fso = FileSystemObject(file[0]).to_dict()
        fso['search'] = text
        fso['text_found'] = file[2]
        fso['page_num'] = file[1]
        output.append(fso)

    return output
