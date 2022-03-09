import datetime
from uuid import uuid4
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
# from pypi_org.data.releases import Release


class Inventory(SqlAlchemyBase):
    __tablename__ = 'inventory'

    inventory_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid4()).replace('-', ''))
    library_id = sa.Column(sa.String, sa.ForeignKey('library.library_id'), index=True)
    parent = orm.relationship("Library", back_populates="inventory")
    inventory_add_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    inventory_modified_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    inventory_removed_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    full_path = sa.Column(sa.String, nullable=False)
    directory = sa.Column(sa.String, nullable=False)
    object_type = sa.Column(sa.String)
    is_hidden = sa.Column(sa.BOOLEAN)
    is_image = sa.Column(sa.BOOLEAN)
    is_raw_image = sa.Column(sa.BOOLEAN)
    is_video = sa.Column(sa.BOOLEAN)
    is_audio = sa.Column(sa.BOOLEAN)
    folder = sa.Column(sa.String)
    file = sa.Column(sa.String)
    file_extension = sa.Column(sa.String)
    file_mime_type = sa.Column(sa.String)
    file_count = sa.Column(sa.BIGINT)
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


    # # releases relationship
    # releases: List[Release] = orm.relation("Release", order_by=[
    #     Release.major_ver.desc(),
    #     Release.minor_ver.desc(),
    #     Release.build_ver.desc(),
    # ], back_populates='package')

    def __repr__(self):
        return f"Inventory {self.id}"
