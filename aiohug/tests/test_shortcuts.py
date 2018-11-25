import json

import pytest
from aiohttp import web

from aiohug.shortcuts import process_response


def test_plaintext():
    text = "pong"
    resp = process_response(text)
    expected = web.Response(text=text)
    assert resp.text == expected.text
    assert resp.content_type == expected.content_type


@pytest.mark.parametrize("body", ({"message": "hello"}, [{"message": "hello"}]))
def test_json(body):
    response = process_response(body)
    expected_response = web.Response(
        text=json.dumps(body), content_type="application/json"
    )
    assert response.body == expected_response.body
    assert response.content_type == expected_response.content_type


@pytest.mark.parametrize("body", ({"message": "hello"}, [{"message": "hello"}]))
def test_status_and_body(body):
    status = 201
    response = process_response((status, body))
    expected_response = web.Response(
        text=json.dumps(body), content_type="application/json", status=status
    )
    assert response.status == expected_response.status
    assert response.body == expected_response.body


@pytest.mark.parametrize("body", [5, 5.0, web.Response(text="not shorted")])
def test_not_short_response(body):
    assert process_response(body) == body
