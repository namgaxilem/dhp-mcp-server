from app.main.mcp_servers.thumbnail.server import mcp

import app.main.mcp_servers.thumbnail.tools.thumbnail

# Entry point to run the server
if __name__ == "__main__":
    mcp.run(transport='streamable-http')
