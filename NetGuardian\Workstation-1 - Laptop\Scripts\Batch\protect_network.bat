@echo off
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
)

echo Running network protection measures with elevated privileges...

:: Reset network settings to default
netsh winsock reset
netsh int ip reset
netsh winhttp reset proxy

:: Clear ARP cache
arp -d *

:: Clear DNS cache
ipconfig /flushdns

:: Disable proxy settings
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f

:: Reset all network adapters
ipconfig /release
ipconfig /renew

:: Enable Windows Firewall
netsh advfirewall set allprofiles state on

:: Block common proxy ports
netsh advfirewall firewall add rule name="Block_Proxy_8080" dir=in action=block protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Block_Proxy_3128" dir=in action=block protocol=TCP localport=3128
netsh advfirewall firewall add rule name="Block_Proxy_1080" dir=in action=block protocol=TCP localport=1080

echo Network protection measures completed.
pause