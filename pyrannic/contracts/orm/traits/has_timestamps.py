from datetime import datetime

from pyrannic.contracts.orm.model import ModelInterface


class HasTimestampInterface(ModelInterface):
    __created_at_column_name__ = "created_at"

    def set_created_at(self, created_at: datetime | None) -> None:
        raise NotImplementedError


class HasTimestampsInterface(HasTimestampInterface):
    __updated_at_column_name__ = "updated_at"

    def set_updated_at(self, updated_at: datetime | None) -> None:
        raise NotImplementedError
