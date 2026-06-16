from pyrannic.container.container import T


def scoped(cls: T) -> T:
    """Decorator to register a scoped binding in the container."""

    setattr(cls, "__pyrannic_binding_type__", "scoped")

    return cls
