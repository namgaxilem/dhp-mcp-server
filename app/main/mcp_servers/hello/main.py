from server import mcp

import promts.promt_hello
import tools.alerts
import tools.forecast

# Entry point to run the server
if __name__ == "__main__":
    mcp.run(transport='streamable-http')
