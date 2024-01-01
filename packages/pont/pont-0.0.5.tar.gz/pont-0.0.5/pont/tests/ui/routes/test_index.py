import pytest

from pont.flow import Flow


@pytest.mark.asyncio
async def test_get_index(http_server):
    """
    Test that the index page is rendered, the index is simple
    and just renders a template, this is just a sanity check
    """
    resp = await http_server.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert 'hx-swap="innerHtml"' in text


@pytest.mark.asyncio
async def test_get_search_completion(http_server, database):
    """
    Test that the search completion endpoint is working
    """
    database.flows().add(Flow("http", id="1", path="/hello", method="GET"))

    resp = await http_server.post("/search/completion", json={"q": "method="})
    assert resp.status == 200
    data = await resp.json()
    assert len(data) > 0
    assert data[0]["kind"] == "value"
    assert data[0]["text"] == "GET"

    resp = await http_server.post("/search/completion", json={"q": "meth"})
    assert resp.status == 200
    data = await resp.json()
    assert len(data) > 0
    assert data[0]["kind"] == "field"
    assert data[0]["text"] == "method"
