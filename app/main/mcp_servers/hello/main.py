from app.main.mcp_servers.hello.server import mcp

import app.main.mcp_servers.hello.promts.promt_hello
import app.main.mcp_servers.hello.tools.alerts
import app.main.mcp_servers.hello.tools.forecast

# Entry point to run the server
if __name__ == "__main__":
    mcp.run(transport='streamable-http')
