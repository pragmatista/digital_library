import sqlalchemy as sa
import sqlalchemy.orm as orm
from uuid import uuid4
from data.modelbase import SqlAlchemyBase


class Metadata(SqlAlchemyBase):
    __tablename__ = 'metadata'
    classification_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid4()).replace('-', ''))
    inventory_id = sa.Column(sa.String, sa.ForeignKey('inventory.inventory_id'), unique=True, nullable=False )
    tag = sa.Column(sa.String, index=True, nullable=False)

    # Indexes
    # <index name> = sa.Index(<index name>, <col_1>, <col 2>..., unique=True, )

    # Relationships
    inv = orm.relationship("Inventory", back_populates="meta")

    def to_dict(self):
        return self.__dict__

    def __iter__(self):
        yield from self.__dict__.values()
