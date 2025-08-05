@echo off
setlocal enabledelayedexpansion

echo Starting MCP Servers...

REM Loop through all subdirectories in app\mcp_servers
for /D %%G in (app\main\mcp_servers\*) do (
    if exist "%%G\main.py" (
        echo Starting server: %%G
        start cmd /k python %%G\main.py
    )
)

echo Starting Proxy Server...
python app\main\mcp_proxy_server\main.py
