import pytest


@pytest.mark.asyncio
async def test_get_config(http_server, settings):
    settings.config_file = "/hello"
    settings.proxies = [{"protocol": "world"}]
    resp = await http_server.get("/config")
    assert resp.status == 200
    text = await resp.text()
    assert "/hello" in text
    assert "world" in text
