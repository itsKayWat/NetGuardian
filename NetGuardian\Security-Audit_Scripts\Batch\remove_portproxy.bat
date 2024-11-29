@echo off
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
)

echo Removing suspicious port forwarding rules with elevated privileges...

:: Remove all port proxy settings
netsh interface portproxy reset

:: Display current settings to verify removal
netsh interface portproxy show all

:: Block the specific port that was being forwarded
netsh advfirewall firewall add rule name="Block_41951" dir=in action=block protocol=TCP localport=41951
netsh advfirewall firewall add rule name="Block_41951_Out" dir=out action=block protocol=TCP remoteport=41951