import datetime
from uuid import uuid4
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase


class Library(SqlAlchemyBase):
    __tablename__ = 'library'

    library_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid4()).replace('-', ''))

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    modified_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    removed_date = sa.Column(sa.DateTime, index=True)
    library_name = sa.Column(sa.String)
    base_path = sa.Column(sa.String)
    description = sa.Column(sa.String)
    user_defined = sa.Column(sa.BOOLEAN, default=True)

    files = orm.relationship("Inventory", back_populates="libraries")

    def to_dict(self):
        return self.__dict__

    def __iter__(self):
        yield from self.__dict__.values()
