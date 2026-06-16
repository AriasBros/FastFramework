from fastapi import APIRouter

from app.http.routers.heroes import router as heroes_router


routers: list[APIRouter] = [
    heroes_router,
]
