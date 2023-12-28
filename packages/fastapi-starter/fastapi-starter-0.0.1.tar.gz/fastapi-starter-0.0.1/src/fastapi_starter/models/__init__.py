from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
    MetaData,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base

naming_conventions = [
    {Index: "IX_%(column_0_label)s"},
    {UniqueConstraint: "UQ_%(table_name)s_%(column_0_name)s"},
    {CheckConstraint: "CK_%(table_name)s_%(constraint_name)s"},
    {
        ForeignKeyConstraint: "FK_%(table_name)s_%(column_0_name)s_%(referred_table_name)s_%(referred_column_0_name)s"
    },
    {PrimaryKeyConstraint: "PK_%(table_name)s"},
]

metadata = MetaData(naming_convention=naming_conventions)
Base = declarative_base(metadata=metadata)

Base.as_dict = lambda self: {
    c.name: getattr(self, c.name) for c in self.__table__.columns
}
