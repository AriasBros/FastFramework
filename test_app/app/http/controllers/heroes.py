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


@router.get(
    "/heroes/{hero_id}",
    summary="Get Hero Endpoint",
    description="Endpoint to retrieve a specific hero by ID.",
)
def show(
    hero_id: str,
    repository: Annotated[HeroesRepository, Depends()],
) -> Hero:
    # where(id=hero_id)
    hero = repository.select().first()

    if not hero:
        raise Exception("Hero not found")  # TODO - Add exception Resource Not Found

    return Hero.from_model(hero)


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
