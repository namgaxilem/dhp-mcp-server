#!/bin/bash

# Bật chế độ thoát khi gặp lỗi
set -e

# Lấy biến môi trường SERVER_NAME
SERVER_NAME="${SERVER_NAME}"

# Nếu SERVER_NAME rỗng -> chạy tất cả
if [ -z "$SERVER_NAME" ]; then
    echo "SERVER_NAME not set, running all MCP servers..."
    run_all=true
else
    # Check SERVER_NAME có trong ROUTE_MAP không
    python - <<EOF
from app.main.router_config import ROUTE_MAP
import sys

name = "${SERVER_NAME}"
if name not in ROUTE_MAP:
    print(f'ERROR: SERVER_NAME "{name}" is not found in ROUTE_MAP.')
    sys.exit(1)
EOF

    echo "SERVER_NAME is \"$SERVER_NAME\", running only that server..."

    # Chạy đúng server
    if [ -f "app/main/mcp_servers/${SERVER_NAME}/main.py" ]; then
        echo "Starting server module: app.main.mcp_servers.${SERVER_NAME}"
        python -m app.main.mcp_servers.${SERVER_NAME}.main &
    else
        echo "ERROR: Folder app/main/mcp_servers/${SERVER_NAME} not found."
        exit 1
    fi

    run_all=false
fi

# Hàm chạy tất cả server
if [ "$run_all" = true ]; then
    echo "Starting MCP Servers..."
    for dir in app/main/mcp_servers/*/; do
        if [ -f "${dir}main.py" ]; then
            modulename=$(basename "$dir")
            echo "Starting server module: app.main.mcp_servers.${modulename}"
            python -m app.main.mcp_servers.${modulename}.main &
        fi
    done
fi

# Chạy Proxy Server
echo "Starting Proxy Server..."
uvicorn app.main.mcp_proxy_server.main:app --reload --host 0.0.0.0 --port 8080
