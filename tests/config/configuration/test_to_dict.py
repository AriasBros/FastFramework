from tests.config.configuration.foo import Foo


def test_to_dict(foo: Foo):
    assert foo.to_dict() == {
        "name": "Pyrannic",
        "env": "production",
        "debug": False,
    }
