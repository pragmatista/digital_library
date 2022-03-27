import datetime
import data.db_session as db_session
from data.inventory import Inventory
from sqlalchemy import desc
from sqlalchemy.sql import func


def refresh_inventory(**kwargs):
    if db := get_inventory_from_path(kwargs.get("full_path")):
        update_inventory(db.inventory_id, **kwargs)
    else:
        add_inventory(**kwargs)


def add_inventory(**kwargs):
    session = db_session.create_session()
    inv = Inventory()
    inv.library_id = kwargs.get("library_id")
    inv.full_path = kwargs.get("full_path")
    inv.directory = kwargs.get("directory")
    inv.object_type = kwargs.get("object_type")
    inv.is_missing = kwargs.get("is_missing")
    inv.is_hidden = kwargs.get("is_hidden")
    inv.is_image = kwargs.get("is_image")
    inv.is_raw_image = kwargs.get("is_raw_image")
    inv.image_contains_text = kwargs.get("image_contains_text")
    inv.image_contains_faces = kwargs.get("image_contains_faces")
    inv.is_video = kwargs.get("is_video")
    inv.is_audio = kwargs.get("is_audio")
    inv.is_document = kwargs.get("is_document")
    inv.folder = kwargs.get("folder")
    inv.folder_count = kwargs.get("folder_count")
    inv.file_count = kwargs.get("file_count")
    inv.file = kwargs.get("file")
    inv.file_extension = kwargs.get("file_extension")
    inv.file_mime_type = kwargs.get("file_mime_type")
    inv.size = kwargs.get("size")
    inv.size_kb = kwargs.get("size_kb")
    inv.size_mb = kwargs.get("size_mb")
    inv.size_gb = kwargs.get("size_gb")
    inv.created_dt = kwargs.get("created_dt")
    inv.created_date_yyyymm = kwargs.get("created_date_yyyymm")
    inv.modified_date_yyyymm = kwargs.get("modified_date_yyyymm")
    inv.modified_dt = kwargs.get("modified_dt")
    inv.opened_dt = kwargs.get("opened_dt")
    inv.owner = kwargs.get("owner")
    inv.group = kwargs.get("group")
    inv.age = kwargs.get("age")

    session.add(inv)
    session.commit()


def update_inventory(inventory_id, **kwargs):
    session = db_session.create_session()
    inv = session.query(Inventory).get(inventory_id)

    inv.library_id = kwargs.get("library_id") or inv.library_id
    inv.inventory_modified_date = datetime.datetime.now()
    inv.inventory_removed_date = kwargs.get("inventory_removed_date") or inv.inventory_removed_date
    inv.inventory_removed_reason = kwargs.get("inventory_removed_reason") or inv.inventory_removed_reason
    inv.is_missing = kwargs.get("is_missing")

    inv.full_path = kwargs.get("full_path") or inv.full_path
    inv.directory = kwargs.get("directory") or inv.directory
    inv.object_type = kwargs.get("object_type") or inv.object_type
    inv.is_hidden = kwargs.get("is_hidden") or inv.is_hidden
    inv.is_image = kwargs.get("is_image") or inv.is_image
    inv.is_raw_image = kwargs.get("is_raw_image") or inv.is_raw_image
    inv.image_contains_text = kwargs.get("image_contains_text") or inv.image_contains_text
    inv.image_contains_faces = kwargs.get("image_contains_faces") or inv.image_contains_faces
    inv.is_video = kwargs.get("is_video") or inv.is_video
    inv.is_audio = kwargs.get("is_audio") or inv.is_audio
    inv.is_document = kwargs.get("is_document") or inv.is_document
    inv.folder = kwargs.get("folder") or inv.folder
    inv.folder_count = kwargs.get("folder_count") or inv.folder_count
    inv.file_count = kwargs.get("file_count") or inv.file_count
    inv.file = kwargs.get("file") or inv.file
    inv.file_extension = kwargs.get("file_extension") or inv.file_extension
    inv.file_mime_type = kwargs.get("file_mime_type") or inv.file_mime_type
    inv.size = kwargs.get("size") or inv.size
    inv.size_kb = kwargs.get("size_kb") or inv.size_kb
    inv.size_mb = kwargs.get("size_mb") or inv.size_mb
    inv.size_gb = kwargs.get("size_gb") or inv.size_gb
    inv.created_dt = kwargs.get("created_dt") or inv.created_dt
    inv.created_date_yyyymm = kwargs.get("created_date_yyyymm") or inv.created_date_yyyymm
    inv.modified_date_yyyymm = kwargs.get("modified_date_yyyymm") or inv.modified_date_yyyymm
    inv.modified_dt = kwargs.get("modified_dt") or inv.modified_dt
    inv.opened_dt = kwargs.get("opened_dt") or inv.opened_dt
    inv.owner = kwargs.get("owner") or inv.owner
    inv.group = kwargs.get("group") or inv.group
    inv.age = kwargs.get("age") or inv.age
    inv.compare_score = kwargs.get("compare_score") or inv.compare_score
    inv.compare_score_dt = kwargs.get("compare_score_dt") or inv.compare_score_dt

    session.commit()


def remove_inventory_item(inventory_id, reason: str):
    session = db_session.create_session()
    inv = session.query(Inventory).get(inventory_id)
    inv.inventory_removed_date = datetime.datetime.now(datetime.timezone.utc)
    inv.inventory_removed_reason = reason
    session.commit()


def get_all_inventory():
    session = db_session.create_session()
    results = session.query(Inventory).all()
    return [result.to_dict() for result in results]


def get_inventory_from_path(full_path) -> Inventory:
    session = db_session.create_session()
    return session.query(Inventory).filter(Inventory.full_path == full_path).first()


def get_library_inventory(library_id):
    session = db_session.create_session()
    results = session.query(Inventory).filter(Inventory.library_id == library_id).all()
    return [result.to_dict() for result in results]


def get_removed_inventory(library_id):
    session = db_session.create_session()
    results = session.query(Inventory)\
        .filter(Inventory.library_id == library_id,
                Inventory.inventory_removed_date != None,
                Inventory.inventory_removed_reason != None,
                Inventory.is_missing == False)\
        .all()
    return [result.to_dict() for result in results]


def get_comparable_inventory(library_id):
    session = db_session.create_session()
    results = (
        session.query(Inventory)
        .filter(
            Inventory.library_id == library_id,
            Inventory.compare_score > 0,
            Inventory.inventory_removed_date == None,
        )
        .order_by(desc(Inventory.compare_score), Inventory.file)
        .all()
    )

    return [result.to_dict() for result in results]


def get_inventory_item(inventory_id) -> Inventory:
    session = db_session.create_session()
    return session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

