import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from uuid import uuid4
from data.modelbase import SqlAlchemyBase


class Inventory(SqlAlchemyBase):
    __tablename__ = 'inventory'

    inventory_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid4()).replace('-', ''))
    library_id = sa.Column(sa.String, sa.ForeignKey('library.library_id'), index=True)
    inventory_add_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    inventory_modified_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    inventory_removed_date = sa.Column(sa.DateTime, index=True)
    inventory_removed_reason = sa.Column(sa.String)
    is_missing = sa.Column(sa.BOOLEAN, default=False)
    full_path = sa.Column(sa.String, unique=True, nullable=False)
    directory = sa.Column(sa.String, nullable=False)
    object_type = sa.Column(sa.String)
    is_hidden = sa.Column(sa.BOOLEAN, default=False)
    is_image = sa.Column(sa.BOOLEAN, default=False)
    is_raw_image = sa.Column(sa.BOOLEAN, default=False)
    image_contains_text = sa.Column(sa.BOOLEAN, default=False)
    image_contains_faces = sa.Column(sa.BOOLEAN, default=False)
    is_video = sa.Column(sa.BOOLEAN, default=False)
    is_audio = sa.Column(sa.BOOLEAN, default=False)
    is_document = sa.Column(sa.BOOLEAN, default=False)
    folder = sa.Column(sa.String)
    folder_count = sa.Column(sa.BIGINT, default=0)
    file_count = sa.Column(sa.BIGINT, default=0)
    file = sa.Column(sa.String)
    file_extension = sa.Column(sa.String)
    file_mime_type = sa.Column(sa.String)
    size = sa.Column(sa.BIGINT)
    size_kb = sa.Column(sa.FLOAT)
    size_mb = sa.Column(sa.FLOAT)
    size_gb = sa.Column(sa.FLOAT)
    created_dt = sa.Column(sa.DATETIME)
    created_date_yyyymm = sa.Column(sa.String)
    modified_date_yyyymm = sa.Column(sa.String)
    modified_dt = sa.Column(sa.DATETIME)
    opened_dt = sa.Column(sa.DATETIME)
    owner = sa.Column(sa.String)
    group = sa.Column(sa.String)
    age = sa.Column(sa.INT)
    compare_score = sa.Column(sa.BIGINT)
    compare_score_dt = sa.Column(sa.DATETIME)

    libraries = orm.relationship("Library", back_populates="files")
    classification = orm.relationship("Classification", back_populates="inv")

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f"Inventory {self.inventory_id}"
