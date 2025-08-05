from fastapi import FastAPI, Request, Response
import httpx
from starlette.responses import StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

ROUTE_MAP = {
    "/app1": "http://localhost:9000",
    "/app2": "http://localhost:9001",
}

client = httpx.AsyncClient(timeout=None)


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def reverse_proxy(request: Request, full_path: str):
    matched_prefix = None
    for prefix in ROUTE_MAP:
        if request.url.path.startswith(prefix):
            matched_prefix = prefix
            break

    if not matched_prefix:
        return Response(content="No route mapping found", status_code=404)

    # Remove prefix from path
    backend_base = ROUTE_MAP[matched_prefix]
    forwarded_path = request.url.path[len(matched_prefix):]
    if not forwarded_path.startswith("/"):
        forwarded_path = "/" + forwarded_path

    target_url = f"{backend_base}{forwarded_path}"

    try:
        headers = dict(request.headers)
        body = await request.body()

        # Forward request to backend server
        backend_response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params,
        )

        # Stream the response back to client
        return StreamingResponse(
            backend_response.aiter_bytes(),
            status_code=backend_response.status_code,
            headers=dict(backend_response.headers),
        )

    except httpx.HTTPError as e:
        return Response(content=f"Proxy Error: {str(e)}", status_code=502)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
