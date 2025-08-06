@echo off
setlocal enabledelayedexpansion

echo Starting MCP Servers...

REM Lặp qua tất cả subdirectories trong app\main\mcp_servers
for /D %%G in (app\main\mcp_servers\*) do (
    if exist "%%G\main.py" (
        REM Lấy tên thư mục con (tên module)
        for %%H in (%%G) do set "modulename=%%~nH"

        echo Starting server module: app.main.mcp_servers.!modulename!
        start cmd /k python -m app.main.mcp_servers.!modulename!.main
    )
)

echo Starting Proxy Server...
uvicorn app.main.mcp_proxy_server.main:app --reload
