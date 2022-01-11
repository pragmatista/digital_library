import os
import mimetypes
import pathlib
from datetime import datetime, timezone, date


def get_folder_name(path):
    if os.path.isdir(path):
        return os.path.basename(os.path.normpath(path))


def get_folder_path(path):
    return os.path.dirname(os.path.abspath(path))


def get_file_name(path):
    if os.path.isfile(path):
        return os.path.basename(os.path.normpath(path))


def get_creation_date(path):
    modified_date = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
    birth_date = datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc)
    if birth_date > modified_date:
        return modified_date
    else:
        return birth_date


def get_modified_date(path):
    return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)


def get_opened_date(path):
    return datetime.fromtimestamp(os.stat(path).st_atime, tz=timezone.utc)


def get_size(path):
    if os.path.isfile(path):
        return os.stat(path).st_size
    else:
        return 0


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
    if os.path.isfile(path):
        return pathlib.Path(path).suffix.lower()
    else:
        return None


def get_mime_type(path):
    if os.path.isfile(path):
        return mimetypes.guess_type(path, strict=False)[0]
    else:
        return None


def get_object_type(path):
    if os.path.isdir(path):
        return "Folder"
    else:
        return "File"


def get_is_file(path):
    return os.path.isfile(path)


def get_is_image(path):
    img_formats = ['.raw', '.dng', '.heic', '.sr2', '.orf', '.crw', '.jpg', '.png', '.gif', '.jpeg']
    file_extension = get_file_extension(path)
    mime_type = str(get_mime_type(path)).lower().startswith('image')

    return mime_type or file_extension in img_formats


def get_is_video(path):
    return str(get_mime_type(path)).lower().startswith('video')


def get_is_audio(path):
    return str(get_mime_type(path)).lower().startswith('audio')


def get_is_raw_image(path):
    raw_formats = ['.raw', '.dng', '.heic', '.sr2', '.orf', '.crw']
    file_extension = get_file_extension(path)

    return file_extension in raw_formats


def get_is_hidden(path):
    return os.path.basename(os.path.normpath(path))[0] == '.'


def get_owner(path):
    return pathlib.Path(path).owner()


def get_group(path):
    return pathlib.Path(path).group()


def get_age_in_years(eval_date):
    days_in_year = 365.2425
    return int((date.today() - eval_date).days / days_in_year)


def get_creation_date_yyyymm(path):
    modified_date = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
    birth_date = datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc)
    if birth_date > modified_date:
        return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc).strftime('%Y-%m')
    else:
        return datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc).strftime('%Y-%m')


def get_modified_date_yyyymm(path):
    return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc).strftime('%Y-%m')


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
        self.folder: str = get_folder_name(path)
        self.file: str = get_file_name(path)
        self.file_extension: str = get_file_extension(path)
        self.file_mime_type: str = get_mime_type(path)
        self.file_count: int = 0
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
        self.age: int = get_age_in_years(self.modified_dt.date())

    def to_dict(self):
        return self.__dict__


