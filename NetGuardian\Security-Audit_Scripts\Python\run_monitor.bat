@echo off
title Network Protection Monitor
color 0A

:: Request admin privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:start
cls
echo Network Protection Monitor
echo =============================
echo Started at: %date% %time%
echo.

:: Create log file
set "logfile=network_monitor_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.log"
echo Network Monitor Log > "%logfile%"
echo Started at: %date% %time% >> "%logfile%"

:monitor
echo Checking network status...
echo.

:: Check network connections
netstat -ano >> "%logfile%"
echo Network connections checked at %time% >> "%logfile%"

:: Check port forwarding rules
echo Checking port forwarding rules...
netsh interface portproxy show all >> "%logfile%"

:: Check for specific suspicious port (41951)
netstat -ano | find "41951" >> "%logfile%"
if %errorlevel% EQU 0 (
    echo [ALERT] Suspicious port 41951 detected! >> "%logfile%"
    echo [ALERT] Suspicious port 41951 detected!
)

:: Check proxy settings
netsh winhttp show proxy >> "%logfile%"

:: Display current status
echo Last check: %time%
echo Log file: %logfile%
echo.
echo Press Q to quit or any other key to check again...
choice /c QX /t 10 /d X /n >nul
if errorlevel 2 goto monitor
if errorlevel 1 goto end

:end
echo Monitor stopped at: %date% %time% >> "%logfile%"
echo.
echo Monitoring stopped. Check %logfile% for details.
pause