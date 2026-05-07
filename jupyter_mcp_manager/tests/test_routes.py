import json

from tornado.httpclient import HTTPClientError


async def test_get_mcp_servers(jp_fetch):
    response = await jp_fetch("jupyter-mcp-manager", "servers")

    assert response.code == 200
    payload = json.loads(response.body)
    assert "mcp_servers" in payload
    assert isinstance(payload["mcp_servers"], list)
    assert "count" in payload


async def test_get_mcp_servers_reload(jp_fetch):
    response = await jp_fetch("jupyter-mcp-manager", "servers", params={"reload": "true"})

    assert response.code == 200
    payload = json.loads(response.body)
    assert "mcp_servers" in payload
    assert "count" in payload


async def test_get_mcp_server_not_found(jp_fetch):
    try:
        response = await jp_fetch("jupyter-mcp-manager", "servers", "nonexistent")
    except HTTPClientError as e:
        # Expect 404 response
        assert e.code == 404
        return
    # If no exception, check the response
    assert response.code == 404
    if response.body:
        try:
            payload = json.loads(response.body)
            assert "error" in payload
        except (json.JSONDecodeError, TypeError):
            pass
