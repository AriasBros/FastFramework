from typing import Annotated

from fastapi import APIRouter, Depends

from test_app.app.http.resources.hero import Hero, HeroesCollection
from test_app.app.models.hero import Hero as HeroModel
from test_app.app.repositories.heroes import HeroesRepository

router = APIRouter(tags=["Heroes"])


@router.get(
    "/heroes",
    summary="Heroes Endpoint",
    description="Endpoint to retrieve the list of heroes.",
)
def index(
    repository: Annotated[HeroesRepository, Depends()],
) -> HeroesCollection:
    return HeroesCollection(repository.select().get())


@router.post(
    "/heroes",
    summary="Create Hero Endpoint",
    description="Endpoint to create a new hero.",
)
def create(
    repository: Annotated[HeroesRepository, Depends()],
) -> Hero:
    return Hero.from_model(
        repository.create(
            HeroModel(
                name="Superman",
                description="The Man of Steel",
            )
        )
    )
