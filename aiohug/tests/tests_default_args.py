from aiohug.arguments import get_default_args


def test_get_default_args():
    def fn(a, b=5, c=5):
        pass

    assert get_default_args(fn) == {"b": 5, "c": 5}
