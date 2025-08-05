import pytest
from httpx import Response as HTTPXResponse
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import httpx

from main import app, client

test_client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_mock_client():
    """
    Automatically patches the global `client` in `main.py` before each test.
    """
    with patch("main.client", new_callable=AsyncMock) as mock_client:
        yield mock_client


def test_no_route_match():
    response = test_client.get("/unknown/path")
    assert response.status_code == 404
    assert response.text == "No route mapping found"


@pytest.mark.asyncio
async def test_proxy_get(setup_mock_client):
    mock_backend_response = HTTPXResponse(
        status_code=200,
        content=b"Hello from backend",
        headers={"X-Test": "yes"}
    )

    # Configure mock client to return the fake backend response
    setup_mock_client.request.return_value = mock_backend_response

    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/app1/test-path?foo=bar")

    assert response.status_code == 200
    assert response.content == b"Hello from backend"
    assert response.headers.get("x-test") == "yes"

    # Ensure the correct backend URL was built and called
    setup_mock_client.request.assert_awaited_once()
    args, kwargs = setup_mock_client.request.call_args
    assert kwargs["url"] == "http://localhost:9000/test-path"
    assert kwargs["params"].get("foo") == "bar"


@pytest.mark.asyncio
async def test_proxy_post_with_body(setup_mock_client):
    mock_backend_response = HTTPXResponse(
        status_code=201,
        content=b"Created",
    )

    setup_mock_client.request.return_value = mock_backend_response

    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/app2/resource", json={"name": "test"})

    assert response.status_code == 201
    assert response.content == b"Created"

    setup_mock_client.request.assert_awaited_once()
    args, kwargs = setup_mock_client.request.call_args
    assert kwargs["url"] == "http://localhost:9001/resource"
    assert b'"name": "test"' in kwargs["content"]


@pytest.mark.asyncio
async def test_backend_http_error(setup_mock_client):
    setup_mock_client.request.side_effect = httpx.ConnectTimeout("Connection timeout")

    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/app1/failure")

    assert response.status_code == 502
    assert "Proxy Error" in response.text
