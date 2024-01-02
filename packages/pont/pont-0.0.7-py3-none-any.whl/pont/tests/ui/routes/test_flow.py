import pytest

from pont.flow import Flow


@pytest.mark.asyncio
async def test_get_flow(http_server, database):
    database.flows().add(Flow("http", id="1", path="/hello"))
    resp = await http_server.get("/flows/1")
    assert resp.status == 200
    text = await resp.text()
    assert "/hello" in text


@pytest.mark.asyncio
async def test_get_flow_not_found(http_server):
    resp = await http_server.get("/flows/4040404")
    assert resp.status == 404
