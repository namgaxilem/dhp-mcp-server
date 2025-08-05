from server import mcp

# Import tools so they get registered via decorators
import tools.alerts
import tools.forecast

# Entry point to run the server
if __name__ == "__main__":
    # mcp.run(transport='stdio')
    mcp.run(transport='streamable-http')
    # mcp.run(transport='sse')
