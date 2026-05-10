from typing import Any

from fastapi import Depends

from fastframework.contracts.http.request import RequestInterface


class _Resolves:
    def __init__(self, name: str | type | None = None):
        self.name = name

    def __call__(self, request: RequestInterface) -> Any:
        return request.app.container.resolve(self.name)


def Resolves(name: str | type | None = None) -> Any:
    return Depends(_Resolves(name))
