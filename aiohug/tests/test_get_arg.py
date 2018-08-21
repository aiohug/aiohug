from aiohttp import web
import pytest

from aiohug.arguments import get_arg


def test_get_request():
    req = "message_that_should_be_the_same"
    assert get_arg(req, "request") is req


@pytest.mark.skip()
def test_directive():
    assert False


@pytest.mark.skip()
def test_arg_from_path():
    assert False


@pytest.mark.skip()
def test_arg_from_query():
    assert False


@pytest.mark.skip()
def test_order():
    assert False


@pytest.mark.skip()
def test_return_default():
    assert False
