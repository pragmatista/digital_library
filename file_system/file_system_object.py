import os
import mimetypes
import pathlib
from datetime import datetime, timezone, date


class FileSystemObject:
    def __init__(self, path: str):
        self.full_path: str = path
        self.directory: str = get_folder_path(path)
        self.object_type: str = get_object_type(path)
        self.is_hidden: bool = get_is_hidden(path)
        self.is_image: bool = get_is_image(path)
        self.is_raw_image: bool = get_is_raw_image(path)
        self.is_video: bool = get_is_video(path)
        self.is_audio: bool = get_is_audio(path)
        self.is_document: bool = get_is_document(path)
        self.folder: str = get_folder_name(path)
        self.folder_count: int = 0
        self.file_count: int = 0
        self.file: str = get_file_name(path)
        self.file_extension: str = get_file_extension(path)
        self.file_mime_type: str = get_mime_type(path)
        self.size: int = get_size(path)
        self.size_kb: float = get_size_kb(path)
        self.size_mb: float = get_size_mb(path)
        self.size_gb: float = get_size_gb(path)
        self.created_dt: datetime = get_creation_date(path)
        self.created_date_yyyymm: str = get_creation_date_yyyymm(path)
        self.modified_date_yyyymm: str = get_modified_date_yyyymm(path)
        self.modified_dt: datetime = get_modified_date(path)
        self.opened_dt: datetime = get_opened_date(path)
        self.owner: str = get_owner(path)
        self.group: str = get_group(path)
        self.age: int = get_age_in_years(path)
        self.is_found: bool = get_is_found(path)

    def to_dict(self):
        try:
            return self.__dict__
        except FileNotFoundError:
            return None


def get_folder_name(path):
    if os.path.isdir(path):
        return os.path.basename(os.path.normpath(path))


def get_folder_path(path):
    try:
        return os.path.dirname(os.path.abspath(path))
    except FileNotFoundError:
        return None


def get_file_name(path):
    if os.path.isfile(path):
        return os.path.basename(os.path.normpath(path))


def get_creation_date(path):
    try:
        modified_date = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
        birth_date = datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc)
        return modified_date if birth_date > modified_date else birth_date
    except FileNotFoundError:
        return None


def get_modified_date(path):
    try:
        return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
    except FileNotFoundError:
        return None


def get_opened_date(path):
    try:
        return datetime.fromtimestamp(os.stat(path).st_atime, tz=timezone.utc)
    except FileNotFoundError:
        return None


def get_size(path):
    try:
        return os.stat(path).st_size if os.path.isfile(path) else 0
    except FileNotFoundError:
        return None


def get_size_kb(path):
    if os.path.isfile(path):
        size = os.stat(path).st_size
        return round(size / 1024, 3)
    else:
        return 0


def get_size_mb(path):
    if os.path.isfile(path):
        size = os.stat(path).st_size
        return round(size / 1024**2, 3)
    else:
        return 0


def get_size_gb(path):
    if os.path.isfile(path):
        size = os.stat(path).st_size
        return round(size / (1024**2 * 1024), 3)
    else:
        return 0


def get_file_extension(path):
    return pathlib.Path(path).suffix if os.path.isfile(path) else None


def get_mime_type(path):
    if os.path.isfile(path):
        return mimetypes.guess_type(path, strict=False)[0]
    else:
        return None


def get_object_type(path):
    return "Folder" if os.path.isdir(path) else "File"


def get_is_file(path):
    try:
        return os.path.isfile(path)
    except FileNotFoundError:
        return None


def get_is_image(path):
    try:
        img_formats = ['.raw', '.dng', '.heic', '.sr2', '.orf', '.crw', '.jpg', '.png', '.gif', '.jpeg']
        file_extension = get_file_extension(path)
        mime_type = str(get_mime_type(path)).lower().startswith('image')
        return mime_type or file_extension.lower() in img_formats
    except AttributeError:
        return None


def get_is_video(path):
    try:
        return str(get_mime_type(path)).lower().startswith('video')
    except FileNotFoundError:
        return None


def get_is_audio(path):
    try:
        return str(get_mime_type(path)).lower().startswith('audio')
    except FileNotFoundError:
        return None


def get_is_document(path):
    try:
        return get_is_file(path) \
               and not get_is_audio(path) \
               and not get_is_video(path) \
               and not get_is_image(path) \
               and not get_is_raw_image(path)
    except FileNotFoundError:
        return None


def get_is_raw_image(path):
    try:
        raw_formats = ['.raw', '.dng', '.heic', '.sr2', '.orf', '.crw']
        file_extension = get_file_extension(path).lower()

        return file_extension in raw_formats
    except AttributeError:
        return None


def get_is_hidden(path):
    try:
        return os.path.basename(os.path.normpath(path))[0] == '.'
    except FileNotFoundError:
        return None


def get_owner(path):
    try:
        return pathlib.Path(path).owner()
    except FileNotFoundError:
        return None


def get_group(path):
    try:
        return pathlib.Path(path).group()
    except FileNotFoundError:
        return None


def get_age_in_years(path):
    try:
        if eval_date := get_modified_date(path).date():
            days_in_year = 365.2425
            return int((date.today() - eval_date).days / days_in_year)
    except AttributeError:
        return None


def get_creation_date_yyyymm(path):
    try:
        modified_date = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
        birth_date = datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc)
        if birth_date > modified_date:
            return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc).strftime('%Y-%m')
        else:
            return datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc).strftime('%Y-%m')
    except FileNotFoundError:
        return None


def get_modified_date_yyyymm(path):
    try:
        return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc).strftime('%Y-%m')
    except FileNotFoundError:
        return None


def get_is_found(path):
    return bool(os.path.isfile(path)) or bool(os.path.isdir(path))



