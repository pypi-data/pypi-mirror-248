import aiohttp.web
import pytest
import pytest_asyncio

from pont.flow import Flow


@pytest_asyncio.fixture
async def flows_server(http_server, database) -> aiohttp.web.Application:
    database.flows().add(Flow("http", id="1", path="/hello"))
    database.flows().add(Flow("http", id="2", path="/world"))
    database.flows().add(Flow("redis", id="3", path="akey"))
    return http_server


@pytest.mark.asyncio
async def test_get_flows(flows_server, database):
    resp = await flows_server.get("/components/flows")
    assert resp.status == 200
    text = await resp.text()
    assert "/hello" in text
    assert "/world" in text
    assert "akey" in text
    assert (
        resp.headers["Last-Modified"]
        == database.flows().find(reverse=True)[0].updated_at.isoformat()
    )


@pytest.mark.asyncio
async def test_get_flows_with_filter(flows_server):
    resp = await flows_server.get("/components/flows?q=protocol%3Dhttp")
    assert resp.status == 200
    text = await resp.text()
    assert "/hello" in text
    assert "/world" in text
    assert "akey" not in text


@pytest.mark.asyncio
async def test_get_flows_with_htmx_headers(flows_server):
    resp = await flows_server.get(
        "/components/flows?q=protocol%3Dhttp", headers={"HX-Current-URL": "/hello"}
    )
    assert resp.status == 200
    assert resp.headers["HX-Replace-Url"] == "/hello?q=protocol%3Dhttp"


@pytest.mark.asyncio
async def test_get_flows_with_if_modified_since(flows_server, database):
    flow = Flow("http", id="1", path="/hello")
    database.flows().add(flow)
    resp = await flows_server.get(
        "/components/flows?q=protocol%3Dhttp",
        headers={"If-Modified-Since": flow.updated_at.isoformat()},
    )
    assert resp.status == 304


@pytest.mark.asyncio
async def test_get_flows_with_if_modified_since_but_no_flows(flows_server, database):
    flow = Flow("http", id="1", path="/hello")
    database.flows().clear()
    resp = await flows_server.get(
        "/components/flows?q=protocol%3Dhttp",
        headers={"If-Modified-Since": flow.updated_at.isoformat()},
    )
    assert resp.status == 200


@pytest.mark.asyncio
async def test_delete_flows(flows_server, database):
    resp = await flows_server.delete("/components/flows")
    assert resp.status == 200
    text = await resp.text()
    assert "/hello" not in text
