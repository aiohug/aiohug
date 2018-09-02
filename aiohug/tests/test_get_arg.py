import asyncio

from aiohttp import web
import pytest

from aiohug.arguments import get_arg
from unittest.mock import MagicMock


def test_get_request():
    request = "message_that_should_be_the_same"
    assert get_arg(request, "request", {}) is request


async def test_directive():
    body = {"data": {}}
    request = MagicMock()
    request.json = asyncio.coroutine(MagicMock(return_value=body))
    assert await get_arg(request, "body", {}) == body


def test_arg_from_path():
    request = MagicMock()
    request.match_info = {"name": "Lucy"}
    assert get_arg(request, "name", {}) == "Lucy"


def test_arg_from_query():
    request = MagicMock()
    request.match_info = {}
    request.rel_url.query = {"name": "Lucy"}
    assert get_arg(request, "name", {}) == "Lucy"


def test_return_default():
    request = MagicMock()
    request.match_info = {}
    request.rel_url.query = {}

    assert get_arg(request, "name", {"name": 5}) == 5
