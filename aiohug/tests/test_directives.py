from aiohug.directives import get_available_directives


def test_get_directive():
    assert ['body'] == list(get_available_directives().keys())
