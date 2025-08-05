from server import mcp

import tools.thumbnail

# Entry point to run the server
if __name__ == "__main__":
    # mcp.run(transport='stdio')
    mcp.run(transport='streamable-http')
    # mcp.run(transport='sse')
