#!/bin/bash

echo "Starting MCP Servers..."

# Loop through all subdirectories in app/mcp_servers
for dir in app/mcp_servers/*/
do
    if [ -f "${dir}main.py" ]; then
        echo "Starting server: $dir"
        python "${dir}main.py" &
    fi
done

echo "Starting Proxy Server..."
python app/mcp_proxy_server/main.py
