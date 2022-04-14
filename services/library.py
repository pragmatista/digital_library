import data.db_session as db_session
from data.library import Library
import datetime
from sqlalchemy.sql import and_, or_


def add_library(**kwargs):
    session = db_session.create_session()
    lib = Library()
    lib.library_name = kwargs.get("library_name")
    lib.description = kwargs.get("description")
    lib.base_path = kwargs.get("base_path")
    lib.user_defined = kwargs.get("user_defined")
    session.add(lib)
    session.commit()


def update_library(**kwargs):
    if get_library(kwargs.get("library_id")):
        session = db_session.create_session()
        lib = session.query(Library).get(kwargs.get("library_id"))
        lib.library_name = kwargs.get("library_name") or lib.library_name
        lib.description = kwargs.get("description") or lib.description
        lib.base_path = kwargs.get("base_path") or lib.base_path
        lib.user_defined = kwargs.get("user_defined") or lib.user_defined
        session.commit()


def remove_library(library_id):
    session = db_session.create_session()
    lib = session.query(Library).get(library_id)
    lib.removed_date = datetime.datetime.now(datetime.timezone.utc)
    session.commit()


def get_all_libraries() -> list[Library]:
    session = db_session.create_session()
    results = session.query(Library).all()
    return [result.to_dict() for result in results]


def get_user_libraries() -> list[Library]:
    session = db_session.create_session()
    results = session.query(Library).filter(Library.user_defined == True).all()
    return [result.to_dict() for result in results]


def get_library(library_id) -> Library:
    session = db_session.create_session()
    return session.query(Library).get(library_id)


def get_model_training_library() -> Library:
    session = db_session.create_session()
    return session.query(Library).\
        filter(Library.library_name == 'Facial Recognition Model (Training)',
               Library.user_defined == False)\
        .first()


def get_model_testing_library() -> Library:
    session = db_session.create_session()
    return session.query(Library).\
        filter(Library.library_name == 'Facial Recognition Model (Testing)',
               Library.user_defined == False)\
        .first()


def get_model_libraries():
    session = db_session.create_session()
    results = session.query(Library).filter(and_(Library.user_defined == False,
                                                 Library.library_name.like("%facial%"))).all()
    return [result.to_dict() for result in results]
