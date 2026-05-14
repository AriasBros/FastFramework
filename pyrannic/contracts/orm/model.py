from typing import Any


class ModelInterface:
    def __pre_init__(self, **kwargs: Any):
        pass

    def __post_init__(self, **kwargs: Any):
        pass
