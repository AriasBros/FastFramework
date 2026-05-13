from fastapi.exceptions import RequestValidationError


class PagesExceededError(RequestValidationError):
    """
    Exception raised when a request exceeded the number of pages allowed to be fetched.
    """

    def __init__(self, *loc: str, error_type: str = None, message: str = None):
        super().__init__(
            [
                {
                    "loc": ("query", *loc),
                    "msg": message or "field exceeds the last page",
                    "type": error_type or "value_error.page_exceeded",
                }
            ]
        )
