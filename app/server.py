from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DHP MCP Server", stateless_http=True, host="0.0.0.0", port=8000)

# from tools.alerts import get_alerts
# from tools.forecast import get_forecast
# from tools.thumbnail import generate_thumbnail

# mcp.add_tool(get_alerts)
# mcp.add_tool(get_forecast)
# mcp.add_tool(generate_thumbnail)

# if __name__ == "__main__":
#     # mcp.run(transport='stdio')
#     mcp.run(transport='streamable-http')
#     # mcp.run(transport='sse')