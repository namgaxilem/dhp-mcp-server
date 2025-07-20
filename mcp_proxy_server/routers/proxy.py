from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
import httpx

router = APIRouter()

# Mapping route prefix to target port
ROUTE_MAP = {
    "app1": "http://localhost:9000",
    "app2": "http://localhost:9001",
    "app3": "http://localhost:9002",
}

@router.api_route("/{proxy_prefix}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
@router.api_route("/{proxy_prefix}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def reverse_proxy(proxy_prefix: str, request: Request, path: str = ""):
    base_url = ROUTE_MAP.get(proxy_prefix)
    if not base_url:
        raise HTTPException(status_code=404, detail="Proxy target not found")

    forward_url = f"{base_url}/{path}"

    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=forward_url,
                headers=headers,
                content=body,
                params=request.query_params,
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=str(e))

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
