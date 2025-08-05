from server import mcp

@mcp.prompt()
def hello_promt():
    return "Hello, this is a prompt from the hello server!"