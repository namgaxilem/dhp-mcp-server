from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import httpx
from starlette.background import BackgroundTask

app = FastAPI()

# Example route map: you can expand this
ROUTE_MAP = {
    "app1": "http://localhost:8080",
    "app2": "http://localhost:9090",
}


@app.api_route("/{app}/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def reverse_proxy(app: str, full_path: str, request: Request):
    if app not in ROUTE_MAP:
        return Response(content="Unknown app", status_code=404)

    # Build the destination URL
    destination_base = ROUTE_MAP[app].rstrip("/")
    dest_url = f"{destination_base}/{full_path}"

    # Copy headers, remove hop-by-hop and problematic ones
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in {"host", "content-length", "accept-encoding", "connection"}
    }
    headers.setdefault("accept", "*/*")  # Avoid 406 Not Acceptable

    # Prepare request body (if any)
    body = await request.body()

    # Send request to target server
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.request(
                method=request.method,
                url=dest_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=None,
                stream=True,
            )
        except httpx.RequestError as exc:
            return Response(content=f"Upstream server error: {exc}", status_code=502)

        # For error status codes, read and return content directly
        if response.status_code >= 400 or response.headers.get("content-length") == "0":
            error_content = await response.aread()
            return Response(
                content=error_content,
                status_code=response.status_code,
                headers={
                    k: v for k, v in response.headers.items()
                    if k.lower() not in {"content-encoding", "transfer-encoding", "connection"}
                },
            )

        # For success, stream the response
        async def stream_response():
            try:
                async for chunk in response.aiter_raw():
                    yield chunk
            except httpx.StreamClosed:
                return

        return StreamingResponse(
            stream_response(),
            status_code=response.status_code,
            headers={
                k: v for k, v in response.headers.items()
                if k.lower() not in {"content-encoding", "transfer-encoding", "connection"}
            },
            background=BackgroundTask(response.aclose),
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("proxy:app", host="127.0.0.1", port=8080, reload=True)