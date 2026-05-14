from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from pyrannic.contracts.orm.model import ModelInterface
from pyrannic.support.datetime import get_current_utc_datetime


class HasTimestamp(ModelInterface):
    __created_at_column_name__ = "created_at"

    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            name=self.__created_at_column_name__,
        )

    def __pre_init__(self, **kwargs: Any):
        super().__pre_init__(**kwargs)
        self.created_at = kwargs.get("created_at") or get_current_utc_datetime()


class HasTimestamps(HasTimestamp):
    __updated_at_column_name__ = "updated_at"

    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.current_timestamp(),
            name=self.__updated_at_column_name__,
        )

    def __pre_init__(self, **kwargs: Any):
        super().__pre_init__(**kwargs)
        self.updated_at = kwargs.get("updated_at") or self.created_at
