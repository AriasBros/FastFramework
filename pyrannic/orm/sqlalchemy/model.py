from typing import Any

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase

from pyrannic.orm.abstract_model import AbstractModel
from pyrannic.orm.sqlalchemy.serializable import Serializable


class Model(DeclarativeBase, AbstractModel, Serializable):
    __abstract__ = True

    def __init__(self, **kwargs: Any):
        self.__pre_init__(**kwargs)
        self.registry.constructor(self, **kwargs)
        self.__post_init__(**kwargs)

    @classmethod
    def tablename(cls) -> str:
        return super(Model, cls).tablename()

    __tablename__ = tablename

    def is_dirty(self, *attrs: str) -> bool:
        state = inspect(self)
        len_attrs = len(attrs)

        for attr in state.attrs:
            if (len_attrs == 0 or attr.key in attrs) and attr.history.has_changes():
                return True

        return False

    def is_clean(self, *attrs: str) -> bool:
        return not self.is_dirty(*attrs)
