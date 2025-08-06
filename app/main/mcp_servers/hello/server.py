from mcp.server.fastmcp import FastMCP

from app.main.router_config import ROUTE_MAP

mcp = FastMCP(ROUTE_MAP["hello"]["mcpServerName"], 
              stateless_http=True, 
              host="0.0.0.0", 
              port=ROUTE_MAP["hello"]["port"])