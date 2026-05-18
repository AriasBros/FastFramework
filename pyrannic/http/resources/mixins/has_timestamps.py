from datetime import datetime

from pydantic import BaseModel, Field

from pyrannic.support.datetime import encode_datetime_to_iso_8601_with_z_suffix


class DatetimeConfig:
    json_encoders = {
        datetime: encode_datetime_to_iso_8601_with_z_suffix,
    }


class HasDatetimeConfig(BaseModel):
    class Config:
        json_encoders = {
            datetime: encode_datetime_to_iso_8601_with_z_suffix,
        }


class HasTimestamp(HasDatetimeConfig):
    created_at: datetime = Field()


class HasTimestamps(HasTimestamp):
    updated_at: datetime = Field()
