from datetime import datetime
from backend.src.app.foundation.datetime import (
    encode_datetime_to_iso_8601_with_z_suffix,
)
from pydantic import Field, BaseModel


class HasTimestamp(BaseModel):
    created_at: datetime = Field()

    class Config:
        json_encoders = {
            datetime: encode_datetime_to_iso_8601_with_z_suffix,
        }


class HasTimestamps(HasTimestamp):
    updated_at: datetime = Field()
