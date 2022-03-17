import data.db_session as db_session
from data.library import Library


def add_library(**kwargs):
    session = db_session.create_session()
    lib = Library()
    lib.library_name = kwargs.get("library_name")
    lib.description = kwargs.get("description")
    lib.base_path = kwargs.get("base_path")
    session.add(lib)
    session.commit()


def update_library(**kwargs):
    if get_library(kwargs.get("library_id")):
        session = db_session.create_session()
        lib = session.query(Library).get(kwargs.get("library_id"))
        lib.library_name = kwargs.get("library_name") or lib.library_name
        lib.description = kwargs.get("description") or lib.description
        lib.base_path = kwargs.get("base_path") or lib.base_path
        session.commit()


def remove_library():
    pass


def get_all_libraries() -> list[Library]:
    session = db_session.create_session()
    results = session.query(Library).all()
    return [result.to_dict() for result in results]


def get_library(library_id) -> Library:
    session = db_session.create_session()
    return session.query(Library).get(library_id)