import numpy as np
import cv2
import os
import pathlib
import shutil
import subprocess
import re

from file_system.file_system_object import FileSystemObject
from file_system import file_system_object


files_found = 0
files_saved = 0
files_ignored = 0


def copy_file(src_path: str, file: str, dest_folder: str):
    global files_saved

    save_to = os.path.join(dest_folder, file)

    if os.stat(src_path).st_size > 0:
        if os.path.exists(save_to):
            file_suffix = file_system_object.get_file_extension(src_path)
            new_file_name = file.replace(file_suffix, '') + '-DX' + file_suffix
            copy_file(src_path, new_file_name, dest_folder)
        else:
            pathlib.Path(dest_folder).mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, save_to)

        files_saved += 1


def find_files(src: FileSystemObject, search_folder: str):
    file_suffix = src.file_extension
    file_name = src.file

    wildcard_search = '*' + file_name.lower().replace(file_suffix, '') + '*'

    cmd = ["find", search_folder, "-iname", wildcard_search]
    results = subprocess_to_list(cmd)
    return len(results) > 0, results


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


def conditional_copy(src: FileSystemObject, list_of_files: list, dest_folder: str):
    # check to see if we should proceed with copy or just ignore
    allow = True

    for file in list_of_files:
        dest = FileSystemObject(file)

        if src.is_image:
            # Evaluate photos
            src.image_array = decode_image(src.full_path)
            dest.image_array = decode_image(dest.full_path)

            allow = mse(src.image_array, dest.image_array) != 0  # false indicates exact duplicate

        elif (
                # file very likely to be the exact same
                src.created_dt == dest.created_dt
                and src.modified_dt == dest.modified_dt
                and src.file_extension == dest.file_extension
                and src.file_mime_type.lower() == dest.file_mime_type.lower()
                and src.size == dest.size):
            allow = False

        # file has same name but appears to have been modified
        elif src.modified_dt < dest.modified_dt:
            allow = True

        if allow:
            copy_file(src.full_path, src.file, dest_folder)


def adjust_dest_path(path):
    replace('/photos/', '', path)
    replace('/photos/compressed/', '', path)
    replace('/photos/raw/', '', path)
    replace('/videos/', '', path)
    return path


def backup_files(src: str, dest: str, device: str = 'unspecified-device'):
    global files_found, files_saved
    dest = adjust_dest_path(dest)

    files_found = 0
    files_saved = 0

    for root, folders, files in os.walk(src, topdown=True):
        for file in files:
            files_found += 1
            dest_folder = dest
            src_fso = FileSystemObject(os.path.join(root, file))

            if not src_fso.is_hidden:
                if src_fso.is_raw_image:
                    dest_folder += '/Photos' \
                                   + '/' + src_fso.created_date_yyyymm[:4] \
                                   + '/' + src_fso.created_date_yyyymm  \
                                   + '/' + 'Raw' \
                                   + '/' + device
                elif src_fso.is_image:
                    dest_folder += '/Photos' \
                                   + '/' + src_fso.created_date_yyyymm[:4] \
                                   + '/' + src_fso.created_date_yyyymm \
                                   + '/' + 'Compressed' \
                                   + '/' + device
                elif src_fso.is_video:
                    dest_folder += '/Videos' \
                                   + '/' + src_fso.created_date_yyyymm[:4] \
                                   + '/' + src_fso.created_date_yyyymm \
                                   + '/' + device
                elif src_fso.is_audio:
                    dest_folder += '/Audio' \
                                   + '/' + src_fso.created_date_yyyymm[:4] \
                                   + '/' + src_fso.created_date_yyyymm \
                                   + '/' + device
                else:
                    src_path = src_fso.directory
                    dest_folder += src_path.replace(src, '')  # copy folder hierarchy as is

                # derive the destination location (destination folder + file)
                find_matches = find_files(src_fso, dest_folder)
                if find_matches[0]:  # at least 1 match was found
                    conditional_copy(src_fso, find_matches[1], dest_folder)
                else:
                    copy_file(src_fso.full_path, file, dest_folder)

    print(f"Task completed. {files_found} files were found. {files_saved} files were copied.")


def calculate_compare_score(filepath, compression=100, size=0):
    # Function that searches the folder for image files, converts them to a matrix
    try:
        image = decode_image(filepath, compression)
        return np.sum(np.array(image))
    except:
        return size


def decode_image(filepath, compression=100):
    # create images matrix
    try:
        img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if type(img) == np.ndarray:
            img = img[..., 0:3]
            img = cv2.resize(img, dsize=(compression, compression), interpolation=cv2.INTER_CUBIC)
        return img
    except:
        return None


def mse(imageA, imageB):
    try:
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err
    except:
        return None
