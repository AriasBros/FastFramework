from datetime import datetime

from sqlalchemy import DateTime, ColumnElement
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.hybrid import hybrid_property

from pyrannic.contracts.orm.traits.can_be_soft_deleted import CanBeSoftDeletedInterface


class CanBeSoftDeleted(CanBeSoftDeletedInterface):
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="The date when the model has been deleted; NULL if not deleted.",
    )

    def set_deleted_at(self, deleted_at: datetime | None) -> None:
        self.deleted_at = deleted_at

    @hybrid_property
    def is_deleted(self) -> bool:  # type: ignore
        return self.deleted_at is not None

    @is_deleted.inplace.expression
    @classmethod
    def _is_deleted_expression(cls) -> ColumnElement[bool]:
        return cls.deleted_at.isnot(None)
