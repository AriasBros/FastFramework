from typing import Annotated, Any, Callable

from annotated_doc import Doc
from fastapi import APIRouter, Depends
from fastapi.types import DecoratedCallable

from test_app.app.http.resources.hero import HeroesCollection
from test_app.app.repositories.heroes import HeroesRepository


def get(
    summary: Annotated[
        str | None,
        Doc(
            """
                A summary for the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
        ),
    ] = None,
    description: Annotated[
        str | None,
        Doc(
            """
                A description for the *path operation*.

                If not provided, it will be extracted automatically from the docstring
                of the *path operation function*.

                It can contain Markdown.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
        ),
    ] = None,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        def _decorator(instance: Any, *args: Any, **kwargs: Any) -> Any:
            print("self is %s" % instance)
            return self.__router__.get(func)

        return _decorator

    return decorator


class HeroesController:
    __router__ = APIRouter(tags=["Heroes"])

    @get(
        summary="Heroes Endpoint",
        description="Endpoint to retrieve the list of heroes.",
    )
    def index(
        self,
        repository: Annotated[HeroesRepository, Depends()],
    ) -> HeroesCollection:
        return HeroesCollection(repository.select().paginate())
