@echo off
setlocal enabledelayedexpansion

REM Load SERVER_NAME từ biến môi trường
set "SERVER_NAME=%SERVER_NAME%"

REM Nếu SERVER_NAME không được set hoặc rỗng => chạy bình thường
if "%SERVER_NAME%"=="" (
    echo SERVER_NAME not set, running all MCP servers...
    goto run_all
)

REM Đọc ROUTE_MAP từ file router_config.py bằng Python
for /f "usebackq delims=" %%A in (`python -c "from app.main.router_config import ROUTE_MAP; import sys; name=sys.argv[1]; sys.exit(0) if name in ROUTE_MAP else sys.exit(1)" "%SERVER_NAME%"`) do (
    set "CHECK_RESULT=%%A"
)

REM Kiểm tra kết quả trả về từ Python (0 là có, 1 là không)
if errorlevel 1 (
    echo ERROR: SERVER_NAME "%SERVER_NAME%" is not found in ROUTE_MAP.
    exit /b 1
)

echo SERVER_NAME is "%SERVER_NAME%", running only that server...

REM Chạy đúng folder theo SERVER_NAME
if exist "app\main\mcp_servers\%SERVER_NAME%\main.py" (
    echo Starting server module: app.main.mcp_servers.%SERVER_NAME%
    start cmd /k python -m app.main.mcp_servers.%SERVER_NAME%.main
) else (
    echo ERROR: Folder app\main\mcp_servers\%SERVER_NAME% not found.
    exit /b 1
)

goto start_proxy


:run_all
echo Starting MCP Servers...
for /D %%G in (app\main\mcp_servers\*) do (
    if exist "%%G\main.py" (
        for %%H in (%%G) do set "modulename=%%~nH"
        echo Starting server module: app.main.mcp_servers.!modulename!
        start cmd /k python -m app.main.mcp_servers.!modulename!.main
    )
)

:start_proxy
echo Starting Proxy Server...
uvicorn app.main.mcp_proxy_server.main:app --reload --host 0.0.0.0 --port 8080
