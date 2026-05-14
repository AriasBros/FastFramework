import logging

from pydantic import Field

from pyrannic import Configuration


class DatabaseConfig(Configuration):
    default: str = Field(default="sqlite", alias="connection")
    """Here you may specify which of the database connections below you wish 
    to use as your default connection for database operations. This is 
    the connection which will be utilized unless another connection
    is explicitly specified when you execute a query / statement."""

    handlers: list[logging.Handler] = Field(
        default_factory=lambda: [logging.StreamHandler()]
    )
    """A list of logging handlers to use for the application.
    Handlers determine where the log messages are output, such as to the console, a file, or a remote logging server."""

    @property
    def env_prefix(self) -> str:
        return "DB_"
