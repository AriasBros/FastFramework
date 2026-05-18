from datetime import datetime

from pydantic import Field

from pyrannic.http.resources.mixins.has_timestamps import HasDatetimeConfig


class SoftDeletes(HasDatetimeConfig):
    deleted_at: datetime | None = Field(
        default=None,
        description="The timestamp when the resource was soft-deleted. Null if not deleted.",
    )
