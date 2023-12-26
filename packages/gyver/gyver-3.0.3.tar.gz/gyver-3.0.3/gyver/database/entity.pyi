import typing

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, registry

class AbstractEntity:

    metadata: typing.ClassVar[sa.MetaData]
    registry: registry

    def __init__(self, **kwargs: typing.Any) -> None: ...
    @classmethod
    def __tablename__(cls) -> str: ...
    @classmethod
    def classname(cls) -> str: ...

class Entity(AbstractEntity):
    id_: Mapped[int]


def make_table(
    name: str, *args: sa.schema.SchemaItem, **kwargs: typing.Any
) -> sa.Table: ...
