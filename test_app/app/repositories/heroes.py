from pyrannic.orm.sqlalchemy.repository import Repository
from test_app.app.models.hero import Hero


class HeroesRepository(Repository[Hero]):
    __model__ = Hero
