
import os
import pathlib
import shutil
import subprocess
import re

from file_system.file_system_object import FileSystemObject
from file_system import file_system_object
from file_system import images

files_found = 0
files_saved = 0
files_ignored = 0


def adjust_dest_path(path):
    replace('/photos/', '', path)
    replace('/photos/compressed/', '', path)
    replace('/photos/raw/', '', path)
    replace('/videos/', '', path)
    return path


def derive_destination_path(src_fso: file_system_object, src: str, dest: str, device: str = 'unspecified-device'):
    if src_fso.is_raw_image:
        return dest + '/Photos' \
               + '/' + src_fso.created_date_yyyymm[:4] \
               + '/' + src_fso.created_date_yyyymm \
               + '/' + 'Raw' \
               + '/' + device
    elif src_fso.is_image:
        return dest + '/Photos' \
               + '/' + src_fso.created_date_yyyymm[:4] \
               + '/' + src_fso.created_date_yyyymm \
               + '/' + 'Compressed' \
               + '/' + device
    elif src_fso.is_video:
        return dest + '/Videos' \
               + '/' + src_fso.created_date_yyyymm[:4] \
               + '/' + src_fso.created_date_yyyymm \
               + '/' + device
    elif src_fso.is_audio:
        return dest + '/Audio' \
               + '/' + src_fso.created_date_yyyymm[:4] \
               + '/' + src_fso.created_date_yyyymm \
               + '/' + device
    else:
        return dest + '/Documents' \
               + '/' + src_fso.directory.replace(src, '') \
               # + '/' + src_fso.created_date_yyyymm[:4] \
               # + '/' + src_fso.created_date_yyyymm \
        # src_path = src_fso.directory
        # dest += src_path.replace(src, '')  # copy folder hierarchy as is


def find_files(src: FileSystemObject, search_folder: str):
    file_suffix = src.file_extension
    file_name = src.file

    wildcard_search = '*' + file_name.lower().replace(file_suffix, '') + '*'

    cmd = ["find", search_folder, "-iname", wildcard_search]
    return subprocess_to_list(cmd)


def subprocess_to_list(cmd: list):
    """
    Return the output of a process to a list of strings.
    """
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE).stdout.splitlines()


def replace(old, new, text: str, caseinsentive=False):
    if caseinsentive:
        return text.replace(old, new)
    else:
        return re.sub(re.escape(old), new, text, flags=re.IGNORECASE)


def copy_file(src_path: str, file: str, dest_folder: str):
    global files_saved

    # src_dir = os.path.dirname(os.path.abspath(src_path))
    save_to = os.path.join(dest_folder, file)

    try:
        if os.stat(src_path).st_size > 0 and compare_files(src_path, save_to):
            while os.path.exists(save_to):
                file_stem = pathlib.Path(save_to).stem
                file_suffix = file_system_object.get_file_extension(save_to)
                new_file = f'{file_stem}-DX{file_suffix}'
                save_to = os.path.join(dest_folder, new_file)
                if not os.path.exists(save_to):
                    break

    except FileNotFoundError:
        print(f"Missing File Error: {save_to}")

    finally:
        print(f"Source File: {src_path}")
        print(f"Copied File: {save_to}")
        pathlib.Path(dest_folder).mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, save_to)
        files_saved += 1


def compare_files(src: str, dest: str):
    src_fso = FileSystemObject(src)
    dest_fso = FileSystemObject(dest)

    try:
        if (
            # file very likely to be the exact same
                src_fso.created_dt == dest_fso.created_dt
                and src_fso.modified_dt == dest_fso.modified_dt
                and src_fso.file_extension.lower() == dest_fso.file_extension.lower()
                and src_fso.file_mime_type.lower() == dest_fso.file_mime_type.lower()
                and src_fso.size == dest_fso.size):

            return False

        elif src_fso.modified_dt < dest_fso.modified_dt:
            return True

        else:
            return True
    except:
        return True


def allow_copy(src: FileSystemObject, dest_folder: str):
    allow = True

    # find files that have a similar naming pattern to avoid potential duplicates

    if not (matches := find_files(src, dest_folder)):
        return allow

    for file in matches:
        dest = FileSystemObject(file)

        if src.is_image and src.file_extension == dest.file_extension:
            # Evaluate photos
            src.image_array = images.decode_image(src.full_path)
            dest.image_array = images.decode_image(dest.full_path)

            allow = images.mse(src.image_array, dest.image_array) != 0  # false indicates exact duplicate

        elif (
                # file very likely to be the exact same
                src.created_dt == dest.created_dt
                and src.modified_dt == dest.modified_dt
                and src.file_extension.lower() == dest.file_extension.lower()
                and src.file_mime_type.lower() == dest.file_mime_type.lower()
                and src.size == dest.size):
            allow = False

        # file name is the same but appears to have been modified
        elif src.modified_dt < dest.modified_dt:
            allow = True

        else:
            return allow

    return allow


def upload_files(src: str, dest: str, save_option: int = 0):
    global files_found, files_saved
    files_found = 0
    files_saved = 0
    dest_folder = dest

    for root, folders, files in os.walk(src, topdown=True):
        for file in files:
            files_found += 1
            src_fso = FileSystemObject(os.path.join(root, file))

            if not src_fso.is_hidden and src_fso.file:
                print(f"Source File Evaluated: {src_fso.full_path} | {src_fso.is_hidden}")

                if not save_option or save_option == 0:
                    save_option = get_save_option()

                elif save_option.isnumeric() and int(save_option) in range(3):
                    if save_option == 1:
                        device = input("Specify device/hardware name (if any, or leave blank): ")
                        dest = adjust_dest_path(dest)
                        dest_folder = derive_destination_path(src_fso, src, dest, device.strip())
                    elif save_option == 2:  # copy folder hierarchy as is
                        dest += src_fso.full_path.replace(src, '')
                    elif save_option == 3:  # straight copy of file into dest folder
                        dest_folder = dest

                if allow_copy(src_fso, dest_folder):
                    copy_file(src_fso.full_path, file, dest_folder)

    print(f"Task completed. {files_found} files were found. {files_saved} files were copied.")


def get_save_option():
    print("\n")
    print("Save Options | Choose 1 of the following:")
    print("[1] Organize folders by date")
    print("[2] Retain sub-folder(s) from source path")
    print("[3] Straight copy into destination folder")
    return input("> ")

