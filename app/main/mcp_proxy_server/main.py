from fastapi import FastAPI, Request, Response
import httpx
from starlette.responses import StreamingResponse

from app.main.router_config import ROUTE_MAP

app = FastAPI()

client = httpx.AsyncClient(timeout=None)


@app.api_route("/{app_name}/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def reverse_proxy(request: Request, app_name: str, full_path: str):
    if app_name not in ROUTE_MAP:
        return Response(content="No route mapping found", status_code=404)

    backend_port = ROUTE_MAP[app_name]["port"]
    backend_base = f"http://localhost:{backend_port}"

    target_url = f"{backend_base}/{full_path}"

    try:
        headers = dict(request.headers)
        body = await request.body()

        backend_response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params,
        )

        return StreamingResponse(
            backend_response.aiter_bytes(),
            status_code=backend_response.status_code,
            headers=dict(backend_response.headers),
        )

    except httpx.HTTPError as e:
        return Response(content=f"Proxy Error: {str(e)}", status_code=502)
