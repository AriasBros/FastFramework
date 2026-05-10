from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    """
    This class is a trait/mixin to use in an actual request implementation to add pagination support.

    The class adds the following attributes to the request:

        - page: Indicate which page is being requested.
        - per_page: Tell us how many items there are in each page.
    """

    page: int = Field(1, ge=1, description="Current page number")
    per_page: int = Field(15, ge=1, description="Number of items per page")
