from typing import Annotated

from fastapi import APIRouter, Depends

from pyrannic import ResourceNotFoundException

from test_app.app.http.controllers.heroes import HeroesController
from test_app.app.http.resources.hero import Hero, HeroesCollection
from test_app.app.models.hero import Hero as HeroModel
from test_app.app.repositories.heroes import HeroesRepository

router = APIRouter(tags=["Heroes"])
controller = HeroesController()


@router.get(
    "/heroes",
    summary="Heroes Endpoint",
    description="Endpoint to retrieve the list of heroes.",
)
def index(
    repository: Annotated[HeroesRepository, Depends()],
) -> HeroesCollection:
    return HeroesCollection(repository.select().paginate())


@router.get(
    "/heroes/{hero_id}",
    summary="Get Hero Endpoint",
    description="Endpoint to retrieve a specific hero by ID.",
)
def show(
    hero_id: str,
    repository: Annotated[HeroesRepository, Depends()],
) -> Hero:
    hero = repository.select().filter_by(id=hero_id).first()

    if not hero:
        raise ResourceNotFoundException(hero_id)

    return Hero.from_model(hero)


@router.delete(
    "/heroes/{hero_id}",
    summary="Delete Hero Endpoint",
    description="Endpoint to delete a specific hero by ID.",
    status_code=204,
)
def destroy(
    hero_id: str,
    repository: Annotated[HeroesRepository, Depends()],
) -> None:
    hero = repository.find_by_id(hero_id)

    if not hero:
        raise ResourceNotFoundException(hero_id)

    repository.destroy(hero)


@router.post(
    "/heroes",
    summary="Create Hero Endpoint",
    description="Endpoint to create a new hero.",
)
def create(repository: Annotated[HeroesRepository, Depends()]) -> Hero:
    return Hero.from_model(
        repository.create(
            HeroModel(
                name="Superman",
                description="The Man of Steel",
            )
        )
    )
