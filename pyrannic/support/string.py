import re


def to_snake_case(value: str) -> str:
    """Convert a string to snake case."""

    value = (
        re.sub(r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]", " ", value).strip().replace(" ", "_")
    )

    return "".join(value.lower())
