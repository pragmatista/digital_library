import sqlalchemy as sa
import sqlalchemy.orm as orm
from uuid import uuid4
from data.modelbase import SqlAlchemyBase


class Classification(SqlAlchemyBase):
    __tablename__ = 'classification'
    classification_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid4()).replace('-', ''))
    inventory_id = sa.Column(sa.String, sa.ForeignKey('inventory.inventory_id'), unique=True, nullable=False )
    model_classification = sa.Column(sa.String, index=True, nullable=False)
    tags = sa.Column(sa.JSON)

    # Indexes
    # <index name> = sa.Index(<index name>, <col_1>, <col 2>..., unique=True, )

    # Relationships
    inv = orm.relationship("Inventory", back_populates="classification")

    def to_dict(self):
        return self.__dict__

    def __iter__(self):
        yield from self.__dict__.values()
