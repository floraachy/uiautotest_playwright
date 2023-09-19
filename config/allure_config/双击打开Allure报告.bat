@echo off
setlocal enabledelayedexpansion

set "chrome_path="
set reg_query_command=reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" /ve

for /f "tokens=2*" %%A in ('%reg_query_command%') do (
    if "%%A"=="REG_SZ" (
        set "tmp_chrome_path=%%B"
        if exist "!tmp_chrome_path!" (
            set "chrome_path=%%B"
        )
    )
)


if defined chrome_path (
    echo Chrome found at: "%chrome_path%"
    "%chrome_path%" --disable-web-security --user-data-dir="%~dp0/tmp" %~dp0/index.html
) else (
    echo Chrome not found.
    echo start a webserver ...
    start /b http_server.exe -port 5001
    start /WAIT msedge.exe http://127.0.0.1:5001
)
