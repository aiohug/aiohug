import pytest

from aiohug.swagger import get_summary, where_is_parameter


def test_get_summary():
    doc = """Some string
    
    Hello
    """
    assert get_summary(doc) == "Some string"


def test_get_summary_for_empty_string():
    assert get_summary("") == ""


def test_get_summary_for_none():
    assert get_summary(None) == None


@pytest.mark.parametrize(
    "name,url,place",
    (
        ("page_id", "https://example.com/page/{page_id}?published=False", "path"),
        ("page_id", "https://example.com/page/?page_id=5&published=False", "query"),
    ),
)
def test_where_is_parameter(name, url, place):
    assert where_is_parameter(name, url) == place
